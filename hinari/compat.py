"""Startup compatibility check: behavioral, no model names anywhere.

Runs before any Discord connection. Pass returns silently; fail raises
CompatError naming the probe so the user knows to try another model.
"""

from __future__ import annotations

import json

from . import config
from .adapters import llm

PROBE_TOOL: dict = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
            "additionalProperties": False,
        },
    },
}


class CompatError(Exception):
    """Raised with probe=<name> reason=<short> when the model is unusable."""

    def __init__(self, probe: str, reason: str) -> None:
        self.probe = probe
        self.reason = reason
        super().__init__(f"[{probe}] {reason}")


def _check_payload_shape() -> None:
    """Local probe: our own builder must stay owner-locked (no extra params)."""
    payload = llm.build_payload("probe-model", [{"role": "system", "content": "hi"}], [PROBE_TOOL])
    extra = set(payload) - llm.ALLOWED_PAYLOAD_KEYS
    if extra:
        raise CompatError("payload-shape", f"forbidden keys: {sorted(extra)}")
    if payload.get("temperature") != 1:
        raise CompatError("payload-shape", "temperature must be 1")
    if llm.strip_trailer('{"a":1}data: [DONE]') != '{"a":1}':
        raise CompatError("payload-shape", "trailer strip broken")


def check_compatible(base_url: str, api_key: str, model: str,
                       tool_choice: str = "auto", timeout: int = config.COMPAT_TIMEOUT) -> None:
    """Run basic-call + closed-loop probes against the configured endpoint."""
    _check_payload_shape()

    # Probe 1: the model must actually call a tool with valid JSON args.
    probe_messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the weather in Tokyo? Use the tool."},
    ]
    payload = llm.build_payload(model, probe_messages, [PROBE_TOOL], tool_choice)
    try:
        body = llm.post(base_url, api_key, payload, timeout)
        message, finish = llm.parse_message(body)
    except llm.LLMError as exc:
        raise CompatError("basic-call", f"request failed: {exc}") from exc
    if finish != "tool_calls" or not message["tool_calls"]:
        raise CompatError("basic-call", "model returned no tool_calls")
    first = message["tool_calls"][0]
    if first["name"] != "get_weather" or "city" not in first["args"]:
        raise CompatError("basic-call", "wrong tool or args")
    call_id = first["id"]
    if not call_id:
        raise CompatError("basic-call", "tool call has no id")

    # Probe 2: the model must close the loop using a string tool result.
    tool_text = json.dumps({"city": "Tokyo", "temp_c": 28, "condition": "Partly cloudy"})
    follow_up = [
        *probe_messages,
        {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": call_id,
                    "type": "function",
                    "function": {
                        "name": "get_weather",
                        "arguments": json.dumps(first["args"]),
                    },
                }
            ],
        },
        {"role": "tool", "tool_call_id": call_id, "content": tool_text},
        {"role": "user", "content": "Answer with the weather in one short sentence."},
    ]
    payload = llm.build_payload(model, follow_up, [PROBE_TOOL], tool_choice)
    try:
        body = llm.post(base_url, api_key, payload, timeout)
        message, finish = llm.parse_message(body)
    except llm.LLMError as exc:
        raise CompatError("closed-loop", f"request failed: {exc}") from exc
    if finish != "stop":
        raise CompatError("closed-loop", f"expected stop, got {finish}")
    if not isinstance(message["content"], str) or not message["content"].strip():
        raise CompatError("closed-loop", "empty final content")

    # Probe 3: heart warnings ride the tool channel on dangling ids (E4 pattern).
    # A provider that 400s here cannot run heart's miss discipline.
    dangling = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Say the word plum once."},
        {"role": "assistant", "content": "plum?"},
        {"role": "tool", "tool_call_id": "call_heart_probe_0",
         "content": "WARNING: You did not call the tool."},
        {"role": "user", "content": "Noted. Reply with OK."},
    ]
    try:
        body = llm.post(base_url, api_key,
                         {"model": model, "messages": dangling, "temperature": 1}, timeout)
        llm.parse_message(body)
    except llm.LLMError as exc:
        raise CompatError("dangling-tool", f"request failed: {exc}") from exc
