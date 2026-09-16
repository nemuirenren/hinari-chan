"""CALL_LLM via stdlib urllib. Single HTTP place for the whole bot.

Payload rules (owner-locked): exactly model/messages/tools/tool_choice plus
temperature=1. Nothing else is ever sent.
"""

from __future__ import annotations

import json
import re
import urllib.request

from .. import config

_DONE_TRAILER = re.compile(r"\s*data:\s*\[DONE\]\s*$")

ALLOWED_PAYLOAD_KEYS = frozenset({"model", "messages", "tools", "tool_choice", "temperature"})

# The six Hinari tools (LLD section 4) as Chat Completions function specs.
TOOLS: list[dict] = [
    {
        "type": "function",
        "function": {
            "name": "read_chat",
            "description": "Read the latest chat bubbles in the room.",
            "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "scroll_chat",
            "description": "Read older chat bubbles starting at offset from newest.",
            "parameters": {
                "type": "object",
                "properties": {"offset": {"type": "integer", "minimum": 0}},
                "required": ["offset"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_chat",
            "description": "Search room text, or jump to a picked hit with context.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "pick": {"type": "integer", "minimum": 0},
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "send_message",
            "description": "Send 1-10 chat bubbles. reply_to quotes a room message_id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "bubbles": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "text": {"type": "string"},
                                "reply_to": {"type": "integer"},
                            },
                            "required": ["text"],
                            "additionalProperties": False,
                        },
                    }
                },
                "required": ["bubbles"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "do_activity",
            "description": "Go busy/sleep until a local HH:MM time. No requests while away.",
            "parameters": {
                "type": "object",
                "properties": {
                    "label": {"type": "string"},
                    "until": {"type": "string", "description": "Local time HH:MM, e.g. 23:30"},
                },
                "required": ["label", "until"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "memory",
            "description": "List, read, or write long-term memory files (1KB max).",
            "parameters": {
                "type": "object",
                "properties": {
                    "op": {"type": "string", "enum": ["list", "read", "write"]},
                    "name": {"type": "string"},
                    "text": {"type": "string"},
                },
                "required": ["op"],
                "additionalProperties": False,
            },
        },
    },
]


class LLMError(Exception):
    """Raised for transport, protocol, or shape failures."""


def strip_trailer(raw: str) -> str:
    """Remove a stray SSE `[DONE]` trailer some proxies append to JSON bodies."""
    return _DONE_TRAILER.sub("", raw)


def build_payload(
    model: str,
    messages: list[dict],
    tools: list[dict] | None = None,
    tool_choice: str = "auto",
    temperature: float = config.TEMPERATURE,
) -> dict:
    """Build the request body. Only the owner-locked keys are ever present."""
    payload: dict = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "tool_choice": tool_choice,
    }
    if tools is not None:
        payload["tools"] = tools
    assert set(payload) <= ALLOWED_PAYLOAD_KEYS, "forbidden payload key"
    assert payload["temperature"] in (config.TEMPERATURE, config.HEART_TEMPERATURE)
    return payload


def post(base_url: str, api_key: str, payload: dict, timeout: int = 60) -> dict:
    """POST one chat-completions request and return the decoded body."""
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + api_key,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except Exception as exc:
        raise LLMError(f"transport failed: {type(exc).__name__}") from exc
    try:
        return json.loads(strip_trailer(raw))
    except json.JSONDecodeError as exc:
        raise LLMError("unparseable response body") from exc


def parse_message(body: dict) -> tuple[dict, str]:
    """Return (message, finish_reason). Drops provider extras like reasoning.

    message is {"role": "assistant", "content": str|None,
                "tool_calls": [{"id":..., "name":..., "args": dict}]}.
    Raises LLMError when tool args are not valid JSON (caller counts a miss).
    """
    try:
        choice = body["choices"][0]
        raw_msg = choice.get("message", {})
        finish = choice.get("finish_reason", "stop")
    except (KeyError, IndexError, TypeError) as exc:
        raise LLMError("missing choices[0].message") from exc
    calls = []
    for call in raw_msg.get("tool_calls") or []:
        try:
            fn = call["function"]
            args = json.loads(fn.get("arguments") or "{}")
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise LLMError("tool args are not valid JSON") from exc
        calls.append({"id": call.get("id", ""), "name": fn.get("name", ""), "args": args})
    content = raw_msg.get("content")
    return {"role": "assistant", "content": content, "tool_calls": calls}, finish


def call_llm(
    base_url: str,
    api_key: str,
    model: str,
    messages: list[dict],
    tool_choice: str = "auto",
    timeout: int = config.CALL_TIMEOUT,
    tools: list[dict] | None = None,
    temperature: float = config.TEMPERATURE,
) -> tuple[dict, str]:
    """Full CALL_LLM: build, post, parse. Shadows nothing, logs nothing secret."""
    payload = build_payload(model, messages, TOOLS if tools is None else tools,
                            tool_choice, temperature)
    try:
        return parse_message(post(base_url, api_key, payload, timeout))
    except LLMError:
        fallback = "required" if tool_choice == "auto" else "auto"
        payload = build_payload(model, messages, TOOLS if tools is None else tools,
                                fallback, temperature)
        return parse_message(post(base_url, api_key, payload, timeout))
