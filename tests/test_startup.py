"""Startup compatibility-check tests. All provider I/O is faked. No network."""

import json
import unittest
from unittest import mock

from hinari import compat
from hinari.adapters import llm


def canned_post_factory(first_body, second_body):
    calls = {"n": 0}

    def fake_post(base_url, api_key, payload, timeout=60):
        calls["n"] += 1
        assert payload["temperature"] == 1  # owner lock holds even in probes
        return first_body if calls["n"] == 1 else second_body

    return fake_post


def tool_body(call_id="call_1", args=None):
    return {"choices": [{
        "message": {
            "role": "assistant", "content": None,
            "tool_calls": [{
                "id": call_id, "type": "function",
                "function": {"name": "get_weather",
                             "arguments": json.dumps(args or {"city": "Tokyo"})},
            }],
        },
        "finish_reason": "tool_calls",
    }]}


def stop_body(text="It is sunny and 28C in Tokyo."):
    return {"choices": [{
        "message": {"role": "assistant", "content": text},
        "finish_reason": "stop",
    }]}


class CompatTest(unittest.TestCase):
    def test_local_shape_probe_passes(self):
        compat._check_payload_shape()  # must not raise

    def test_happy_path(self):
        fake = canned_post_factory(tool_body(), stop_body())
        with mock.patch.object(compat.llm, "post", fake):
            compat.check_compatible("http://x", "k", "any-model")

    def test_no_tool_calls_fails_basic_probe(self):
        fake = canned_post_factory(stop_body("hi"), stop_body())
        with mock.patch.object(compat.llm, "post", fake):
            with self.assertRaises(compat.CompatError) as ctx:
                compat.check_compatible("http://x", "k", "any-model")
        self.assertEqual(ctx.exception.probe, "basic-call")

    def test_empty_final_content_fails_closed_loop(self):
        fake = canned_post_factory(tool_body(), stop_body("   "))
        with mock.patch.object(compat.llm, "post", fake):
            with self.assertRaises(compat.CompatError) as ctx:
                compat.check_compatible("http://x", "k", "any-model")
        self.assertEqual(ctx.exception.probe, "closed-loop")

    def test_transport_failure_reports_probe(self):
        def boom(*a, **k):
            raise llm.LLMError("down")

        with mock.patch.object(compat.llm, "post", boom):
            with self.assertRaises(compat.CompatError):
                compat.check_compatible("http://x", "k", "any-model")

    def test_configured_tool_choice_reaches_probes(self):
        seen = []

        def fake(base_url, api_key, payload, timeout=60):
            seen.append(payload.get("tool_choice"))
            n = len(seen)
            return tool_body() if n == 1 else stop_body()

        with mock.patch.object(compat.llm, "post", fake):
            compat.check_compatible("http://x", "k", "any-model", tool_choice="required")
        self.assertEqual(seen[0], "required")
        self.assertEqual(seen[1], "required")

    def test_dangling_probe_failure_reports_probe(self):
        seq = {"n": 0}

        def fake(base_url, api_key, payload, timeout=60):
            seq["n"] += 1
            if seq["n"] < 3:
                return tool_body() if seq["n"] == 1 else stop_body()
            raise llm.LLMError("strict 400")

        with mock.patch.object(compat.llm, "post", fake):
            with self.assertRaises(compat.CompatError) as ctx:
                compat.check_compatible("http://x", "k", "any-model")
        self.assertEqual(ctx.exception.probe, "dangling-tool")


if __name__ == "__main__":
    unittest.main()
