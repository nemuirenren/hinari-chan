"""Startup compatibility-check tests. All provider I/O is faked. No network."""

import unittest
from unittest import mock

from hinari import compat
from hinari.adapters import llm


def tool_msg(call_id="call_1", args=None, name="get_weather"):
    return ({"role": "assistant", "content": None,
             "tool_calls": [{"id": call_id, "name": name,
                             "args": args or {"city": "Tokyo"}}]},
            "tool_calls")


def stop_msg(text="It is sunny and 28C in Tokyo."):
    return ({"role": "assistant", "content": text, "tool_calls": []}, "stop")


def canned_call_factory(*items):
    calls = {"n": 0, "seen": []}

    def fake(base_url, api_key, model, messages, tool_choice="auto",
             timeout=240, tools=None, temperature=1):
        calls["n"] += 1
        calls["seen"].append((tool_choice, temperature, bool(tools)))
        assert temperature == 1  # owner lock holds even in probes
        return items[min(calls["n"] - 1, len(items) - 1)]

    fake.calls = calls
    return fake


class CompatTest(unittest.TestCase):
    def test_local_shape_probe_passes(self):
        compat._check_adapter_shape()  # must not raise

    def test_happy_path(self):
        fake = canned_call_factory(tool_msg(), stop_msg(), ({"role": "assistant",
                                                             "content": "OK",
                                                             "tool_calls": []}, "stop"))
        with mock.patch.object(compat.llm, "call_llm", fake):
            compat.check_compatible("http://x", "k", "any-model")

    def test_no_tool_calls_fails_basic_probe(self):
        fake = canned_call_factory(stop_msg("hi"), stop_msg())
        with mock.patch.object(compat.llm, "call_llm", fake):
            with self.assertRaises(compat.CompatError) as ctx:
                compat.check_compatible("http://x", "k", "any-model")
        self.assertEqual(ctx.exception.probe, "basic-call")

    def test_empty_final_content_fails_closed_loop(self):
        fake = canned_call_factory(tool_msg(), stop_msg("   "))
        with mock.patch.object(compat.llm, "call_llm", fake):
            with self.assertRaises(compat.CompatError) as ctx:
                compat.check_compatible("http://x", "k", "any-model")
        self.assertEqual(ctx.exception.probe, "closed-loop")

    def test_transport_failure_reports_probe(self):
        def boom(*a, **k):
            raise llm.LLMError("down")

        with mock.patch.object(compat.llm, "call_llm", boom):
            with self.assertRaises(compat.CompatError):
                compat.check_compatible("http://x", "k", "any-model")

    def test_configured_tool_choice_reaches_probes(self):
        fake = canned_call_factory(tool_msg(), stop_msg(), stop_msg("OK"))
        with mock.patch.object(compat.llm, "call_llm", fake):
            compat.check_compatible("http://x", "k", "any-model", tool_choice="required")
        self.assertEqual([s[0] for s in fake.calls["seen"][:2]], ["required", "required"])

    def test_dangling_probe_failure_reports_probe(self):
        calls = {"n": 0}

        def fake(*a, **k):
            calls["n"] += 1
            if calls["n"] == 1:
                return tool_msg()
            if calls["n"] == 2:
                return stop_msg()
            raise llm.LLMError("strict 400")

        with mock.patch.object(compat.llm, "call_llm", fake):
            with self.assertRaises(compat.CompatError) as ctx:
                compat.check_compatible("http://x", "k", "any-model")
        self.assertEqual(ctx.exception.probe, "dangling-tool")


if __name__ == "__main__":
    unittest.main()
