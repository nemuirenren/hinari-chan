"""Adapter contract tests: LLM payload shape, store, 1-server/1-channel guard.

Stdlib unittest only. No network, no Discord connection.
"""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from hinari import config
from hinari.adapters import llm
from hinari.adapters.discord_phone import Phone
from hinari.adapters.store import FileStore, StoreError


class PhoneBufferTest(unittest.TestCase):
    def test_note_and_backfill_carry_reply_ref(self):
        phone = Phone()
        phone.note_message(1, "rin", 7, 10, "setuju!", False, reply_to=4242, quoted="main?")
        self.assertEqual(phone.messages[0]["reply_to"], 4242)
        self.assertEqual(phone.messages[0]["quoted"], "main?")
        phone.note_message(2, "bo", 8, 11, "halo", False)
        self.assertIsNone(phone.messages[1]["reply_to"])
        phone.backfill([{"id": 1, "from": "rin", "from_id": 7, "time": 10,
                         "text": "setuju!", "mention": False,
                         "reply_to": 4242, "quoted": "main?"}])
        self.assertEqual(len(phone.messages), 2)  # dedup by id, ref kept


class AdapterShapeTest(unittest.TestCase):
    def test_six_hinari_tools_unchanged(self):
        names = [t["function"]["name"] for t in llm.TOOLS]
        self.assertEqual(names, ["read_chat", "scroll_chat", "search_chat",
                                 "send_message", "do_activity", "memory"])

    def test_send_message_is_bubbles_array(self):
        spec = next(t for t in llm.TOOLS if t["function"]["name"] == "send_message")
        props = spec["function"]["parameters"]["properties"]
        self.assertIn("bubbles", props)
        self.assertNotIn("text", props)
        self.assertEqual(props["bubbles"]["type"], "array")

    def test_maps_all_five_roles(self):
        msgs = llm.to_lc_messages([
            {"role": "system", "content": "sys"},
            {"role": "assistant", "content": "lore", "pinned": True},
            {"role": "assistant", "content": None, "tool_calls": [{
                "id": "c1", "type": "function",
                "function": {"name": "read_chat", "arguments": "{}"}}]},
            {"role": "tool", "tool_call_id": "c1", "content": "{}"},
            {"role": "user", "content": "yo"},
        ])
        kinds = [type(m).__name__ for m in msgs]
        self.assertEqual(kinds, ["SystemMessage", "AIMessage", "AIMessage",
                                 "ToolMessage", "HumanMessage"])
        self.assertEqual(msgs[2].tool_calls[0]["name"], "read_chat")
        self.assertEqual(msgs[3].tool_call_id, "c1")

    def test_unknown_role_raises(self):
        with self.assertRaises(llm.LLMError):
            llm.to_lc_messages([{"role": "carrier-pigeon", "content": "x"}])

    def test_bad_history_args_raise(self):
        with self.assertRaises(llm.LLMError):
            llm.to_lc_messages([{"role": "assistant", "content": None, "tool_calls": [{
                "id": "c1", "type": "function",
                "function": {"name": "read_chat", "arguments": "{bad"}}]}])

    def test_ms_conversion(self):
        self.assertEqual(llm._ms(240), 240_000)
        self.assertEqual(llm._ms(1), 1000)


class ParseResponseTest(unittest.TestCase):
    def _resp(self, content=None, tool_calls=None, finish=None):
        from types import SimpleNamespace

        return SimpleNamespace(content=content, tool_calls=tool_calls or [],
                               response_metadata={"finish_reason": finish} if finish else {})

    def test_parses_calls_and_finish(self):
        msg, finish = llm._parse_response(self._resp(
            None, [{"id": "c1", "name": "read_chat", "args": {}}], "tool_calls"))
        self.assertEqual(finish, "tool_calls")
        self.assertEqual(msg["tool_calls"][0], {"id": "c1", "name": "read_chat", "args": {}})

    def test_finish_falls_back_to_shape(self):
        _, finish = llm._parse_response(self._resp("hi", [], None))
        self.assertEqual(finish, "stop")
        _, finish = llm._parse_response(self._resp(
            None, [{"id": "c", "name": "n", "args": {}}], None))
        self.assertEqual(finish, "tool_calls")

    def test_non_string_content_coerced(self):
        msg, _ = llm._parse_response(self._resp(["part"], [], "stop"))
        self.assertIsInstance(msg["content"], str)

    def test_tool_result_must_be_string(self):
        payload = {"tool_call_id": "c1", "content": json.dumps({"a": 1})}
        self.assertIsInstance(payload["content"], str)


class StoreTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = FileStore(Path(self.tmp.name))

    def tearDown(self):
        self.tmp.cleanup()

    def test_write_read_list(self):
        self.store.write_memory("m1", "hello", 10)
        self.assertEqual(self.store.read_memory("m1").splitlines()[-1], "hello")
        self.assertEqual(self.store.list_memories(), ["m1"])

    def test_rejects_over_1kb(self):
        with self.assertRaises(StoreError):
            self.store.write_memory("big", "x" * 2000, 10)

    def test_broken_links(self):
        res = self.store.write_memory("m1", "see [[ghost]]", 10)
        self.assertEqual(res["broken"], ["ghost"])

    def test_no_tmp_leftovers(self):
        self.store.write_memory("m1", "hi", 10)
        leftovers = list(Path(self.tmp.name).rglob("*.tmp"))
        self.assertEqual(leftovers, [])

    def test_harness_snapshot_roundtrip(self):
        self.store.save_harness({"mood": 7})
        self.assertEqual(self.store.load_harness(), {"mood": 7})

    def test_missing_snapshot_is_empty(self):
        self.assertEqual(self.store.load_harness(), {})

    def test_latest_note_tail(self):
        self.assertEqual(self.store.latest_note_tail(), "")
        self.store.write_memory("m1", "l1\nl2", 10)
        self.assertIn("l2", self.store.latest_note_tail())


class GuardTest(unittest.TestCase):
    def _cfg(self):
        with mock.patch.dict(os.environ, {
            "DISCORD_TOKEN": "t", "DISCORD_GUILD_ID": "1", "DISCORD_CHANNEL_ID": "2",
            "LLM_BASE_URL": "http://x", "LLM_API_KEY": "k", "LLM_MODEL": "m",
        }, clear=True):
            return config.Config.from_env()

    def test_allowed_only_exact_pair(self):
        cfg = self._cfg()
        self.assertTrue(config.is_allowed(1, 2, cfg))
        self.assertFalse(config.is_allowed(1, 3, cfg))
        self.assertFalse(config.is_allowed(9, 2, cfg))

    def test_missing_env_lists_names(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(config.ConfigError) as ctx:
                config.Config.from_env()
        self.assertIn("DISCORD_TOKEN", str(ctx.exception))

    def test_tool_choice_default_auto(self):
        with mock.patch.dict(os.environ, {
            "DISCORD_TOKEN": "t", "DISCORD_GUILD_ID": "1", "DISCORD_CHANNEL_ID": "2",
            "LLM_BASE_URL": "http://x", "LLM_API_KEY": "k", "LLM_MODEL": "m",
        }, clear=True):
            self.assertEqual(config.Config.from_env().tool_choice, "auto")

    def test_tool_choice_required_respected(self):
        with mock.patch.dict(os.environ, {
            "DISCORD_TOKEN": "t", "DISCORD_GUILD_ID": "1", "DISCORD_CHANNEL_ID": "2",
            "LLM_BASE_URL": "http://x", "LLM_API_KEY": "k", "LLM_MODEL": "m",
            "TOOL_CHOICE": " Required ",
        }, clear=True):
            self.assertEqual(config.Config.from_env().tool_choice, "required")

    def test_tool_choice_bogus_rejected(self):
        with mock.patch.dict(os.environ, {
            "DISCORD_TOKEN": "t", "DISCORD_GUILD_ID": "1", "DISCORD_CHANNEL_ID": "2",
            "LLM_BASE_URL": "http://x", "LLM_API_KEY": "k", "LLM_MODEL": "m",
            "TOOL_CHOICE": "sometimes",
        }, clear=True):
            with self.assertRaises(config.ConfigError):
                config.Config.from_env()


class FallbackTest(unittest.TestCase):
    def _fake_invoke(self, seen, script):
        def fake(base_url, api_key, model, lc_messages, tools, tool_choice,
                 temperature, timeout_s):
            seen.append(tool_choice)
            item = script[min(len(seen) - 1, len(script) - 1)]
            if isinstance(item, Exception):
                raise item
            return item

        return fake

    def test_auto_falls_back_to_required(self):
        seen = []
        script = [llm.LLMError("boom"),
                  ({"role": "assistant", "content": "hi", "tool_calls": []}, "stop")]
        with mock.patch.object(llm, "_invoke_once", self._fake_invoke(seen, script)):
            _, finish = llm.call_llm("u", "k", "m", [{"role": "system", "content": "x"}])
        self.assertEqual(seen, ["auto", "required"])
        self.assertEqual(finish, "stop")

    def test_temperature_asserted(self):
        with self.assertRaises(AssertionError):
            llm.call_llm("u", "k", "m", [], temperature=0.7)

    def test_model_built_with_ms_timeout_and_no_extras(self):
        captured = {}

        def fake_init(*a, **k):
            captured.update(k)
            raise llm.LLMError("stop-here")

        with mock.patch("langchain.chat_models.init_chat_model", fake_init):
            try:
                llm._build_model("http://x/v1/", "k", "m", 1, 240)
            except llm.LLMError:
                pass
        self.assertEqual(captured["timeout"], 240_000)
        self.assertEqual(captured["temperature"], 1)
        self.assertEqual(captured["max_retries"], 0)
        for forbidden in ("max_tokens", "top_p", "reasoning"):
            self.assertNotIn(forbidden, captured)

    def test_default_timeouts_240(self):
        import inspect

        self.assertEqual(inspect.signature(llm.call_llm).parameters["timeout"].default, 240)
        from hinari import compat

        default = inspect.signature(compat.check_compatible).parameters["timeout"].default
        self.assertEqual(default, 240)
        self.assertEqual(config.HEART_TIMEOUT, 240)


if __name__ == "__main__":
    unittest.main()
