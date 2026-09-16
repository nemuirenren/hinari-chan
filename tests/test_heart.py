"""Heart judge tests: tool contract, warnings, clamps, caps, folding input.

Stdlib unittest only. All LLM I/O is faked. No network.
"""

import unittest
from unittest import mock

from hinari import heart
from hinari.adapters import llm


def body_tool(call_id="c1", arguments='{"assessments": []}'):
    return {"choices": [{
        "message": {
            "role": "assistant", "content": None,
            "tool_calls": [{
                "id": call_id, "type": "function",
                "function": {"name": "update_feelings", "arguments": arguments},
            }],
        },
        "finish_reason": "tool_calls",
    }]}


def body_text(content="oops"):
    return {"choices": [{
        "message": {"role": "assistant", "content": content},
        "finish_reason": "stop",
    }]}


class ContractTest(unittest.TestCase):
    def test_tool_name_and_temperature(self):
        self.assertEqual(heart.HEART_TOOL["function"]["name"], "update_feelings")

    def test_stack_order_pinned_identity(self):
        msgs = heart.build_messages("SYS", "IDENTITY", [{"h": 1}], "BATCH", "SNAP")
        self.assertEqual(msgs[0], {"role": "system", "content": "SYS"})
        self.assertEqual(msgs[1]["content"], "IDENTITY")
        self.assertTrue(msgs[1].get("pinned"))
        self.assertEqual(msgs[-1]["role"], "user")
        self.assertIn("BATCH", msgs[-1]["content"])

    def test_bounds_locked(self):
        self.assertEqual((heart.WARM_LO, heart.WARM_HI), (-4, 2))
        self.assertEqual((heart.REL_LO, heart.REL_HI), (-30, 5))
        self.assertEqual(heart.UPSIDE_DAY_CAP, 8)


class CleanTest(unittest.TestCase):
    def test_clamps_numbers(self):
        a = heart._clean({"sender": "rin", "warmth": 99, "rel_delta": -99})
        self.assertEqual((a["warmth"], a["rel_delta"]), (2, -30))

    def test_drops_bad_items(self):
        self.assertIsNone(heart._clean({"sender": "", "warmth": 1, "rel_delta": 1}))
        self.assertIsNone(heart._clean({"sender": "x", "warmth": "hot", "rel_delta": 1}))
        self.assertIsNone(heart._clean("nope"))


class ApplyTest(unittest.TestCase):
    def test_gain_and_warmth_map(self):
        rel, meta = {"rin": 100}, {}
        felt = heart.apply_assessments(
            rel, meta, 9, [{"sender": "rin", "warmth": 2, "rel_delta": 5, "reason": ""}])
        self.assertEqual(rel["rin"], 105)
        self.assertEqual(felt, {"rin": 2})

    def test_new_name_starts_neutral(self):
        rel, meta = {}, {}
        heart.apply_assessments(rel, meta, 9, [{"sender": "new", "warmth": 0, "rel_delta": 3, "reason": ""}])
        self.assertEqual(rel["new"], 3)

    def test_upside_capped_per_day(self):
        rel, meta = {}, {}
        for _ in range(3):
            heart.apply_assessments(
                rel, meta, 9, [{"sender": "n", "warmth": 0, "rel_delta": 5, "reason": ""}])
        self.assertEqual(rel["n"], 8)
        heart.apply_assessments(rel, meta, 10, [{"sender": "n", "warmth": 0, "rel_delta": 5, "reason": ""}])
        self.assertEqual(rel["n"], 13)  # new day, fresh quota

    def test_downside_uncapped(self):
        rel, meta = {}, {}
        for _ in range(3):
            heart.apply_assessments(
                rel, meta, 9, [{"sender": "n", "warmth": 0, "rel_delta": -30, "reason": ""}])
        self.assertEqual(rel["n"], -90)

    def test_score_clamped(self):
        rel, meta = {"a": 498}, {}
        heart.apply_assessments(rel, meta, 9, [{"sender": "a", "warmth": 0, "rel_delta": 5, "reason": ""}])
        self.assertEqual(rel["a"], 500)


class JudgeFlowTest(unittest.TestCase):
    def _run(self, script):
        calls = {"n": 0}

        def fake(*a, **k):
            calls["n"] += 1
            assert k.get("temperature") == 0.4
            item = script[min(calls["n"] - 1, len(script) - 1)]
            if isinstance(item, Exception):
                raise item
            return llm.parse_message(item)  # real parse, faked transport

        with mock.patch.object(heart.llm, "call_llm", fake):
            out = heart.judge("u", "k", "m", "SYS", "ID", [], "BATCH", "SNAP")
        return out, calls["n"]

    def test_happy_path_empty_means_neutral(self):
        (assessments, additions), n = self._run([body_tool()])
        self.assertEqual(assessments, [])
        self.assertEqual(n, 1)
        self.assertEqual(additions[1]["tool_call_id"], "c1")

    def test_miss_warns_with_heart_id_then_recovers(self):
        (assessments, additions), n = self._run([body_text(), body_tool()])
        self.assertEqual(n, 2)
        self.assertEqual(additions[1]["tool_call_id"], "update_feelings")
        self.assertIn("update_feelings", additions[1]["content"])

    def test_double_miss_fails_open(self):
        (assessments, additions), n = self._run([body_text(), body_text()])
        self.assertEqual(assessments, [])
        self.assertEqual(n, 2)
        self.assertEqual(additions[1]["tool_call_id"], "update_feelings")

    def test_malformed_warns_with_call_id(self):
        bad = body_tool(call_id="c9", arguments='{"nope": 1}')
        (assessments, additions), n = self._run([bad, body_tool()])
        self.assertEqual(n, 2)
        self.assertEqual(additions[1]["tool_call_id"], "c9")
        self.assertIn("Invalid", additions[1]["content"])

    def test_transport_failure_is_miss(self):
        (assessments, _), n = self._run([llm.LLMError("down"), body_tool()])
        self.assertEqual(assessments, [])
        self.assertEqual(n, 2)

    def test_slide_keeps_newest_20_pairs(self):
        full_hist = [m for i in range(25) for m in (
            {"role": "assistant", "content": None, "tool_calls": [{"id": f"c{i}"}]},
            {"role": "tool", "tool_call_id": f"c{i}", "content": "pad"},
        )]
        heart.slide_history(full_hist)
        self.assertEqual(len(full_hist), 40)
        self.assertEqual(full_hist[-1]["tool_call_id"], "c24")


if __name__ == "__main__":
    unittest.main()
