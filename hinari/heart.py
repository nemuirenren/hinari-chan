"""Heart: background judge of how words land on Hinari.

Runs behind the tool loop, never as Hinari's tool, never in her history.
All feedback travels the tool channel (structurally validated); the heart
system prompt carries no warnings. Fail-open: any failure means no change.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from . import config
from .adapters import llm

log = logging.getLogger("hinari.heart")

# Owner-locked bounds (Patch-003).
WARM_LO, WARM_HI = -4, 2
REL_LO, REL_HI = -30, 5
UPSIDE_DAY_CAP = 8  # max total rel gain per sender per day; downside uncapped
REL_MIN, REL_MAX = -500, 500
HEART_ID = "update_feelings"  # tool_call_id used when heart made no call

WARN_NO_CALL = (
    "You did not call update_feelings. If nothing warrants a change, "
    "call it with an empty assessments list."
)
WARN_BAD_ARGS = "Invalid arguments for update_feelings: expected {assessments: [...]}."

HEART_TOOL: dict = {
    "type": "function",
    "function": {
        "name": "update_feelings",
        "description": "Record how someone's words land on Hinari. Empty list means no change.",
        "parameters": {
            "type": "object",
            "properties": {
                "assessments": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "sender": {"type": "string"},
                            "warmth": {"type": "number"},
                            "rel_delta": {"type": "number"},
                            "reason": {"type": "string"},
                        },
                        "required": ["sender", "warmth", "rel_delta"],
                        "additionalProperties": False,
                    },
                }
            },
            "required": ["assessments"],
            "additionalProperties": False,
        },
    },
}


def load_heart_prompt(base: Path) -> str:
    path = base / "HEART.md"
    if not path.is_file():
        raise config.ConfigError(f"Missing required prompt file: {path} (heart)")
    return path.read_text(encoding="utf-8")


def build_messages(
    system_text: str,
    identity: str,
    history: list[dict],
    batch_text: str,
    snapshot_text: str,
) -> list[dict]:
    """Heart stack: system, pinned identity, own sliding history, fresh batch."""
    return [
        {"role": "system", "content": system_text},
        {"role": "assistant", "content": identity, "pinned": True},
        *history,
        {"role": "user", "content": f"{snapshot_text}\n\nJudge these words:\n{batch_text}"},
    ]


def _warn_pair(call_id: str, warning: str) -> list[dict]:
    """Assistant placeholder plus the warning on the tool channel (E4 pattern)."""
    return [
        {"role": "assistant", "content": None, "tool_calls": []},
        {"role": "tool", "tool_call_id": call_id, "content": warning},
    ]


def judge(
    base_url: str,
    api_key: str,
    model: str,
    system_text: str,
    identity: str,
    history: list[dict],
    batch_text: str,
    snapshot_text: str,
) -> tuple[list[dict], list[dict]]:
    """One judgment round. Returns (assessments, history_additions).

    Never raises: transport/parse failures and double misses yield ([], ...).
    History additions keep exact id pairing for the next round.
    """
    messages = build_messages(system_text, identity, history, batch_text, snapshot_text)
    status, calls, additions = _attempt(base_url, api_key, model, messages)
    if status == "ok":
        return calls, additions
    warning = additions  # the exact warning pair for this failure mode
    status2, calls2, additions2 = _attempt(base_url, api_key, model, [*messages, *warning])
    if status2 == "ok":
        return calls2, warning + additions2
    log.info("heart failed twice (%s then %s), no change", status, status2)
    return [], warning


def _attempt(
    base_url: str, api_key: str, model: str, messages: list[dict]
) -> tuple[str, list[dict], list[dict]]:
    """Single heart call. Returns (status, assessments, history_additions).

    Status is ok | miss (no usable tool call) | malformed (bad arguments).
    Malformed carries its warning pair so the caller can retry with it.
    """
    try:
        msg, _ = llm.call_llm(
            base_url, api_key, model, messages,
            tools=[HEART_TOOL], temperature=config.HEART_TEMPERATURE,
            timeout=config.HEART_TIMEOUT,
        )
    except llm.LLMError as exc:
        log.warning("heart call failed: %s", exc)
        return "miss", [], []
    calls = msg.get("tool_calls", [])
    if not calls or calls[0].get("name") != HEART_ID:
        return "miss", [], _warn_pair(HEART_ID, WARN_NO_CALL)
    call = calls[0]
    args = call.get("args", {})
    if not isinstance(args, dict) or not isinstance(args.get("assessments"), list):
        return "malformed", [], _warn_pair(call.get("id", HEART_ID), WARN_BAD_ARGS)
    assessments = [_clean(a) for a in args["assessments"]]
    assessments = [a for a in assessments if a is not None]
    pair = [
        {
            "role": "assistant",
            "content": None,
            "tool_calls": [{
                "id": call.get("id", HEART_ID),
                "type": "function",
                "function": {"name": HEART_ID, "arguments": json.dumps(args, default=str)},
            }],
        },
        {"role": "tool", "tool_call_id": call.get("id", HEART_ID),
         "content": json.dumps({"assessed": len(assessments)})},
    ]
    return "ok", assessments, pair


def _clean(raw) -> dict | None:
    """Validate one assessment; None drops the item. Numbers are clamped."""
    if not isinstance(raw, dict):
        return None
    sender = str(raw.get("sender", "")).strip()
    if not sender:
        return None
    try:
        warmth = float(raw.get("warmth", 0))
        delta = float(raw.get("rel_delta", 0))
    except (TypeError, ValueError):
        return None
    return {
        "sender": sender,
        "warmth": min(WARM_HI, max(WARM_LO, warmth)),
        "rel_delta": min(REL_HI, max(REL_LO, delta)),
        "reason": str(raw.get("reason", ""))[:120],
    }


def apply_assessments(rel: dict, meta: dict, day: int, assessments: list[dict]) -> dict:
    """Fold assessments into rel scores. Returns {sender: warmth} for mood.

    New names start Neutral. Upside is capped per sender per day; downside
    lands in full. Scores stay clamped to [-500, 500].
    """
    warmth: dict = {}
    for a in assessments:
        name = a["sender"]
        if name not in rel:
            rel[name] = 0
        delta = a["rel_delta"]
        if delta > 0:
            key = f"rel_cap:{name}:{day}"
            used = meta.get(key, 0)
            applied = min(delta, UPSIDE_DAY_CAP - used)
            meta[key] = used + max(applied, 0)
        else:
            applied = delta
        rel[name] = min(REL_MAX, max(REL_MIN, rel[name] + applied))
        warmth[name] = a["warmth"]
    return warmth


def slide_history(history: list[dict]) -> None:
    """Heart's own window: newest MAX_PAIRS whole pairs survive (Patch-015)."""
    while len(history) > 2 * config.MAX_PAIRS:
        del history[0:2]
