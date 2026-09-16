"""Pipeline nodes: TRIGGER lives in state.py, the rest here.

Pure LLD section 5 logic. No Discord/network/file imports. DISPATCH works on
plain structures (state.group list + memories dict) so it stays unit-testable.
The Discord mirror send happens in main.py, not here (see main._execute_call):
history only ever appends real delivered utterances (Law 3).
"""

from __future__ import annotations

import json

from .. import config
from .state import State

REL_BANDS: list[tuple[str, int, int]] = [
    ("Profound Hatred", -500, -400),
    ("Hostility", -400, -320),
    ("Resentment", -320, -240),
    ("Distrust", -240, -160),
    ("Discomfort", -160, -80),
    ("Aloofness", -80, -20),
    ("Neutral", -20, 20),
    ("Acquaintance", 20, 80),
    ("Cordiality", 80, 160),
    ("Warmth", 160, 240),
    ("Trust", 240, 320),
    ("Deep Affection", 320, 400),
    ("Devotion", 400, 500),
]


def is_reply_to_own(group: list[dict], reply_to: int | None) -> bool:
    """True when reply_to quotes one of Hinari's own recorded bubbles."""
    if not reply_to:
        return False
    return any(m.get("from") == "hinari" and m.get("message_id") == reply_to for m in group)


def rel_band(score: int) -> str:
    for name, lo, hi in REL_BANDS:
        if lo <= score <= hi or (hi == 500 and score == 500):
            return name
    return "Neutral"


def render_system(
    s: State,
    template: str,
    identity_text: str,
    now_text: str,
    activity_text: str,
    group_meta: str,
    memory_tail: str = "",
    mood_text: str = "",
) -> dict:
    """RENDER_SYSTEM. Full-template substitution: every byte of the owner
    template is kept, placeholders are replaced, unknown tags pass through.
    Values carry counts/flags only, never raw chat text or file lists."""
    text = template
    for key, value in {
        "identity": identity_text,
        "now": now_text,
        "activity": activity_text,
        "group_meta": group_meta,
        "memory_tail": memory_tail,
        "mood": mood_text,
    }.items():
        text = text.replace("{" + key + "}", value)
    return {"role": "system", "content": text}


def pinned_lore(lore_text: str) -> dict:
    """PINNED_LORE. Verbatim owner prose at index 1; never slides, never normalized."""
    return {"role": "assistant", "content": lore_text, "pinned": True}


def normalize(assistant_msg: dict) -> dict:
    """NORMALIZE. Generated content is dropped; only tool_calls are kept.

    A message without tool_calls is a miss (handled by handle_miss) and is
    never appended, with or without content.
    """
    return {"role": "assistant", "content": None, "tool_calls": assistant_msg.get("tool_calls", []),
            "raw_content": assistant_msg.get("raw_content", assistant_msg.get("content"))}


def miss_preview(raw_msg: dict, limit: int = config.MISS_PREVIEW) -> str:
    """Render a bounded preview of a missed message for INFO logs.

    Note: free model text, so it passes through the redact filter like any
    other log line. Kept in pipeline (pure) so it stays unit-testable.
    """
    content = raw_msg.get("raw_content")
    if content is None:
        return "<empty>"
    text = str(content)
    if len(text) > limit:
        return text[:limit] + f"...[+{len(text) - limit} chars]"
    return text if text else "<empty>"


def handle_miss(s: State) -> str:
    """MISS_HANDLER. Retry on the same snapshot up to MISS_MAX, then idle-sleep.

    A miss (content without tool_call) appends nothing, ever.
    """
    s.misses += 1
    if s.misses < config.MISS_MAX:
        return "retry-once"
    s.misses = 0
    s.activity_label, s.activity_until = "idle", s.now_min + config.MISS_SLEEP_MIN
    return "sleep-1min"


def _links(text: str) -> list[str]:
    out: list[str] = []
    i = 0
    while (j := text.find("[[", i)) != -1:
        k = text.find("]]", j)
        if k == -1:
            break
        out.append(text[j + 2 : k])
        i = k + 2
    return out


def dispatch(s: State, memories: dict, call: dict) -> tuple[dict, str | None]:
    """DISPATCH. Returns (tool_result, sleep_flag). Pure state mutation only."""
    name, args = call.get("name", ""), call.get("args", {}) or {}
    if name == "read_chat":
        chats = _annotate(s, s.group[-config.SCREEN :])
        return {"chats": chats}, None
    if name == "scroll_chat":
        off = int(args.get("offset", 0))
        end = max(0, len(s.group) - off)
        chats = _annotate(s, s.group[max(0, end - config.SCREEN) : end])
        return {"chats": chats}, None
    if name == "search_chat":
        query = str(args.get("query", ""))
        hits = [m for m in s.group if query in m.get("text", "")][: config.SEARCH_HITS]
        if "pick" in args:
            idx = int(args["pick"])
            if idx < 0 or idx >= len(hits):
                return {"error": "pick out of range"}, None
            anchor = hits[idx]
            i = next(i for i, m in enumerate(s.group) if m is anchor)
            chats = _annotate(s, s.group[max(0, i - 5) : i + 6])
            return {"chats": chats}, None
        snippets = [
            {"n": n, "message_id": m.get("message_id", 0), "now": format_now(m.get("time", 0)),
             "from": m.get("from"), "snippet": m.get("text", "")[:120]}
            for n, m in enumerate(hits)
        ]
        return {"hits": snippets}, None
    if name == "send_message":
        items = _clean_bubbles(args, {m.get("message_id", 0) for m in s.group})
        if isinstance(items, dict):  # validation warning, no state touched
            return items, None
        s.group.append({
            "message_id": 0,  # patched with the first Discord id by the caller
            "from": "hinari",
            "time": s.now_min,
            "text": "\n".join(it["text"] for it in items),
        })
        s.unread = 0
        return {"delivered": s.now_min, "bubbles": len(items)}, None
    if name == "do_activity":
        label = str(args.get("label", "idle"))
        until = _parse_until(str(args.get("until", "")), s.now_min)
        s.activity_label, s.activity_until = label, until
        return {"sleeping_until": until}, "sleep"
    if name == "memory":
        return _memory(memories, args), None
    return {"error": f"unknown tool {name}"}, None


def format_now(epoch_min: int) -> str:
    """Human-readable twin of the system {now}: weekday, date, time + tz."""
    import datetime as _dt

    return _dt.datetime.fromtimestamp(epoch_min * 60).astimezone().strftime("%a, %Y-%m-%d, %H:%M %z")


def _clean_bubbles(args: dict, known: set[int] | None = None) -> list[dict] | dict:
    """Validate the bubbles array. Returns [{text, reply_to|None}], or WARNING."""
    raw = args.get("bubbles")
    if not isinstance(raw, list) or not raw:
        return {"warning": "Invalid send_message format: expected {bubbles: [{text}, ...]}."}
    items = []
    for b in raw:
        if not isinstance(b, dict):
            return {"warning": "Invalid send_message format: each bubble must be {text}."}
        text = str(b.get("text", "")).strip()
        if not text:
            continue
        reply_to = b.get("reply_to")
        if reply_to is not None and (
            not isinstance(reply_to, int) or isinstance(reply_to, bool) or reply_to <= 0
        ):
            return {"warning": "Invalid reply_to: must be a message_id from the room."}
        items.append({"text": text, "reply_to": reply_to})
    if not items:
        return {"warning": "Invalid send_message format: all bubbles are empty."}
    if len(items) > config.MAX_BUBBLES:
        return {"warning": f"Too many bubbles: max {config.MAX_BUBBLES} per call. Trim and retry."}
    if known is not None:
        for it in items:
            if it["reply_to"] is not None and it["reply_to"] not in known:
                return {"warning": f"Unknown reply_to {it['reply_to']}: not a room message."}
    return items


def _annotate(s: State, bubbles: list[dict]) -> list[dict]:
    out = []
    for b in bubbles:
        score = s.rel.get(b.get("from", ""), 0)
        out.append({
            "message_id": b.get("message_id", 0),
            "from": b.get("from"),
            "now": format_now(b.get("time", 0)),
            "text": b.get("text", ""),
            "rel": f"{rel_band(score)} ({score})",
            "reply_to": b.get("reply_to"),
            "quoted": b.get("quoted"),
        })
    return out


def _parse_until(raw: str, now_min: int) -> int:
    """Parse HH:MM to the next future epoch-minute. Falls back to +60min."""
    try:
        hour, _, minute = raw.strip().partition(":")
        day = now_min // 1440
        target = day * 1440 + int(hour) * 60 + int(minute or 0)
        return target if target > now_min else target + 1440
    except (ValueError, AttributeError):
        return now_min + 60


def _memory(memories: dict, args: dict) -> dict:
    op = args.get("op", "")
    if op == "list":
        return {"files": sorted(memories)}
    if op == "read":
        name = args.get("name", "")
        if name not in memories:
            return {"error": "not found"}
        return {"text": memories[name][: config.MEM_MAX]}
    if op == "write":
        name, body = args.get("name", ""), args.get("text", "")
        if not name:
            return {"error": "missing name"}
        if len(body.encode("utf-8")) > config.MEM_MAX:
            return {"error": "memory >1KB rejected"}
        memories[name] = body
        broken = [p for p in _links(body) if p not in memories and p != name]
        return {"written": name, "broken": broken}
    return {"error": f"unknown memory op {op}"}


def slide_window(s: State) -> None:
    """SLIDE_WINDOW. Pin 0 (lore) is absolute; keep the newest MAX_PAIRS whole
    pairs, drop older ones outright (Patch-015). No token math, no exceptions.
    """
    while len(s.history) > 1 + 2 * config.MAX_PAIRS:
        del s.history[1:3]


def append_pair(s: State, call: dict, result: dict) -> None:
    """APPEND one real call plus its real result, with exact id pairing."""
    s.history.append(
        {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": call.get("id", ""),
                    "type": "function",
                    "function": {
                        "name": call.get("name", ""),
                        "arguments": json.dumps(call.get("args", {}), default=str),
                    },
                }
            ],
        }
    )
    s.history.append(
        {
            "role": "tool",
            "tool_call_id": call.get("id", ""),
            "content": json.dumps(result, default=str),
        }
    )
