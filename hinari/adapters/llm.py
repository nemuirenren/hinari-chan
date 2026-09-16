"""CALL_LLM via LangChain against any OpenAI-compatible endpoint.

Single HTTP place for the whole bot (Patch-017: stdlib urllib retired).
Public surface is unchanged: TOOLS, LLMError, call_llm signature.

Owner locks (enforced, not requested): temperature is only ever 1 (Hinari)
or 0.4 (heart); no max_tokens/top_p/etc are ever configured; tool_choice is
auto|required with a mirrored fallback; timeouts are seconds in, milliseconds
out (LangChain unit).
"""

from __future__ import annotations

import json

from .. import config

# The six Hinari tools (LLD section 4) as Chat Completions function specs.
# Passed verbatim to bind_tools; the framework forwards them untouched.
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


def _ms(seconds: float) -> int:
    """LangChain timeouts are milliseconds; ours are seconds. Convert once."""
    return int(seconds * 1000)


def to_lc_messages(messages: list[dict]) -> list:
    """Map Hinari dicts to LangChain messages. Raises LLMError on bad shapes."""
    from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

    out = []
    for m in messages:
        role = m.get("role")
        if role == "system":
            out.append(SystemMessage(content=m.get("content") or ""))
        elif role == "assistant":
            calls = []
            for c in m.get("tool_calls") or []:
                if "function" in c:  # raw OpenAI form (stored history)
                    fn = c.get("function", {})
                    try:
                        args = json.loads(fn.get("arguments") or "{}")
                    except (TypeError, json.JSONDecodeError) as exc:
                        raise LLMError("tool args are not valid JSON") from exc
                    calls.append({"name": fn.get("name", ""), "args": args,
                                  "id": c.get("id", ""), "type": "tool_call"})
                else:  # normalized form
                    args = c.get("args", {}) or {}
                    if not isinstance(args, dict):
                        raise LLMError("tool args are not a dict")
                    calls.append({"name": c.get("name", ""), "args": args,
                                  "id": c.get("id", ""), "type": "tool_call"})
            out.append(AIMessage(content=m.get("content") or "", tool_calls=calls))
        elif role == "tool":
            content = m.get("content", "")
            if not isinstance(content, str):
                content = json.dumps(content, default=str)
            out.append(ToolMessage(content=content, tool_call_id=m.get("tool_call_id", "")))
        elif role == "user":
            out.append(HumanMessage(content=m.get("content") or ""))
        else:
            raise LLMError(f"unknown role {role}")
    return out


def _build_model(base_url: str, api_key: str, model: str,
                 temperature: float, timeout_s: float):
    """LangChain model against a generic OpenAI-compatible base_url.

    Only temperature/timeout/retries are configured — everything else stays
    at SDK defaults (None = not sent).
    """
    from langchain.chat_models import init_chat_model

    return init_chat_model(
        model=model,
        model_provider="openai",
        base_url=base_url.rstrip("/"),
        api_key=api_key,
        temperature=temperature,
        timeout=_ms(timeout_s),
        max_retries=0,
    )


def _parse_response(resp) -> tuple[dict, str]:
    """Normalize an LC answer to (message, finish_reason). Never raises."""
    try:
        raw_calls = resp.tool_calls or []
    except AttributeError:
        raw_calls = []
    calls = [{"id": t.get("id", ""), "name": t.get("name", ""),
              "args": t.get("args", {}) or {}} for t in raw_calls]
    content = resp.content
    if content is not None and not isinstance(content, str):
        content = json.dumps(content, default=str)
    meta = getattr(resp, "response_metadata", None) or {}
    finish = meta.get("finish_reason") or ("tool_calls" if calls else "stop")
    return {"role": "assistant", "content": content, "tool_calls": calls}, finish


def _invoke_once(base_url: str, api_key: str, model: str, lc_messages: list,
                 tools: list[dict] | None, tool_choice: str,
                 temperature: float, timeout_s: float) -> tuple[dict, str]:
    mdl = _build_model(base_url, api_key, model, temperature, timeout_s)
    bound = mdl.bind_tools(tools, tool_choice=tool_choice) if tools else mdl
    try:
        resp = bound.invoke(lc_messages)
    except Exception as exc:
        raise LLMError(f"transport failed: {type(exc).__name__}") from exc
    try:
        return _parse_response(resp)
    except LLMError:
        raise
    except Exception as exc:
        raise LLMError(f"bad response: {type(exc).__name__}") from exc


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
    """Full CALL_LLM: map, invoke, normalize. Shadows nothing, logs nothing secret."""
    assert temperature in (config.TEMPERATURE, config.HEART_TEMPERATURE)
    spec = TOOLS if tools is None else tools
    try:
        lc_messages = to_lc_messages(messages)
    except LLMError:
        raise
    except Exception as exc:
        raise LLMError(f"bad messages: {type(exc).__name__}") from exc
    try:
        return _invoke_once(base_url, api_key, model, lc_messages, spec,
                            tool_choice, temperature, timeout)
    except LLMError:
        fallback = "required" if tool_choice == "auto" else "auto"
        return _invoke_once(base_url, api_key, model, lc_messages, spec,
                            fallback, temperature, timeout)
