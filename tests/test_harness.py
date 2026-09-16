"""Harness unit tests: LLD sections 5-8 against the real implementation.

Stdlib unittest only. No network, no Discord.
"""

import unittest

from hinari import config
from hinari.harness import pipeline
from hinari.harness.state import (
    State,
    apply_stamina,
    need_wake,
    next_mood,
    rel_decay,
)


def make_state(**kwargs):
    group = [{"message_id": 1000 + i, "from": "ren", "time": i, "text": f"msg {i}"}
             for i in range(30)]
    base = {"now_min": 10, "activity_until": 50, "group": group}
    base.update(kwargs)
    return State(**base)


class TokenCountTest(unittest.TestCase):
    def test_deterministic_and_sized(self):
        from hinari import tokens

        a = tokens.count([{"role": "system", "content": "hello"}])
        self.assertEqual(a, tokens.count([{"role": "system", "content": "hello"}]))
        b = tokens.count([{"role": "system", "content": "hello world, this is longer"}])
        self.assertGreater(b, a)
        self.assertGreater(a, 0)


class TriggerTest(unittest.TestCase):
    def test_asleep_when_nothing_pending(self):
        s = make_state(unread=0, mentioned=False)
        self.assertIsNone(need_wake(s))

    def test_until_reached(self):
        s = make_state(now_min=60, activity_until=50)
        self.assertEqual(need_wake(s), "until-reached")

    def test_mention_interrupts(self):
        s = make_state(mentioned=True)
        self.assertEqual(need_wake(s), "interrupted")

    def test_burst_interrupts(self):
        s = make_state(unread=6, mentioned=False)
        self.assertEqual(need_wake(s), "interrupted")
        s = make_state(unread=5, mentioned=False)
        self.assertIsNone(need_wake(s))

    def test_replied_interrupts(self):
        s = make_state(replied=True)
        self.assertEqual(need_wake(s), "interrupted")

    def test_reply_to_own(self):
        group = [{"message_id": 11, "from": "hinari", "time": 1, "text": "hi"},
                 {"message_id": 12, "from": "ren", "time": 2, "text": "yo"}]
        self.assertTrue(pipeline.is_reply_to_own(group, 11))
        self.assertFalse(pipeline.is_reply_to_own(group, 12))
        self.assertFalse(pipeline.is_reply_to_own(group, 999))
        self.assertFalse(pipeline.is_reply_to_own(group, None))

    def test_stamina_forces_sleep(self):
        s = make_state(stamina=0)
        self.assertEqual(need_wake(s), "force-stamina")

    def test_curfew_flag(self):
        s = make_state()
        self.assertEqual(need_wake(s, curfew_fired=True), "force-01:00")


class RenderTemplateTest(unittest.TestCase):
    def test_full_template_substitution(self):
        s = make_state(unread=3, mentioned=True)
        tpl = ("<role><identity>{identity}</identity><time>{now}</time>"
               "<act>{activity}</act><grp>{group_meta}</grp><mem>{memory_tail}</mem>"
               "<mood>{mood}</mood><custom>x</custom></role>")
        msg = pipeline.render_system(s, tpl, "ID", "NOW", "ACT", "GRP",
                                     memory_tail="MEM", mood_text="MOOD")
        content = msg["content"]
        for token in ("ID", "NOW", "ACT", "GRP", "MEM", "MOOD", "<custom>x</custom>"):
            self.assertIn(token, content)
        for slot in ("{identity}", "{now}", "{mood}"):
            self.assertNotIn(slot, content)

    def test_no_raw_chat_text_leaks(self):
        s = make_state()
        msg = pipeline.render_system(s, "{identity}|{group_meta}", "ID", "N", "A", "G")
        self.assertNotIn("msg 29", msg["content"])


class NormalizeMissTest(unittest.TestCase):
    def test_content_dropped_calls_kept(self):
        msg = pipeline.normalize({"content": "Saya AI siap membantu", "tool_calls": [{"a": 1}]})
        self.assertIsNone(msg["content"])
        self.assertEqual(msg["tool_calls"], [{"a": 1}])

    def test_empty_calls_is_miss_shape(self):
        msg = pipeline.normalize({"content": "hello", "tool_calls": []})
        self.assertEqual(msg["tool_calls"], [])

    def test_retry_up_to_max_then_sleep(self):
        s = make_state()
        for _ in range(config.MISS_MAX - 1):
            self.assertEqual(pipeline.handle_miss(s), "retry-once")
        self.assertEqual(pipeline.handle_miss(s), "sleep-1min")
        self.assertEqual(s.misses, 0)
        self.assertEqual(s.activity_until, s.now_min + config.MISS_SLEEP_MIN)


class DispatchReadTest(unittest.TestCase):
    def test_read_latest_7(self):
        s = make_state()
        res, sleep = pipeline.dispatch(s, {}, {"name": "read_chat"})
        self.assertIsNone(sleep)
        self.assertEqual(len(res["chats"]), 7)
        self.assertEqual(res["chats"][-1]["text"], "msg 29")
        first = res["chats"][0]
        self.assertIn("rel", first)
        self.assertEqual(first["message_id"], 1023)
        self.assertIsInstance(first["now"], str)
        self.assertNotIn("time", first)
        self.assertIsNone(first["reply_to"])
        self.assertIsNone(first["quoted"])

    def test_reply_context_shown(self):
        s = make_state()
        s.group.append({"message_id": 9999, "from": "rin", "time": 5, "text": "setuju!",
                        "reply_to": 1029, "quoted": "msg 29"})
        res, _ = pipeline.dispatch(s, {}, {"name": "read_chat"})
        last = res["chats"][-1]
        self.assertEqual(last["reply_to"], 1029)
        self.assertEqual(last["quoted"], "msg 29")

    def test_scroll_offset(self):
        s = make_state()
        res, _ = pipeline.dispatch(s, {}, {"name": "scroll_chat", "args": {"offset": 7}})
        self.assertEqual(len(res["chats"]), 7)
        self.assertEqual(res["chats"][-1]["text"], "msg 22")

    def test_search_hits_capped(self):
        s = make_state()
        res, _ = pipeline.dispatch(s, {}, {"name": "search_chat", "args": {"query": "msg 1"}})
        self.assertLessEqual(len(res["hits"]), 5)
        hit = res["hits"][0]
        self.assertIn("n", hit)
        self.assertIn("message_id", hit)
        self.assertNotIn("id", hit)
        self.assertIsInstance(hit["now"], str)

    def test_search_pick_centers_picked(self):
        s = make_state()
        res, _ = pipeline.dispatch(
            s, {}, {"name": "search_chat", "args": {"query": "msg 1", "pick": 2}})
        self.assertEqual(len(res["chats"]), 11)
        self.assertEqual(res["chats"][5]["text"], "msg 11")

    def test_search_pick_out_of_range(self):
        s = make_state()
        res, _ = pipeline.dispatch(
            s, {}, {"name": "search_chat", "args": {"query": "msg 1", "pick": 99}})
        self.assertIn("error", res)

    def test_unknown_tool(self):
        s = make_state()
        res, _ = pipeline.dispatch(s, {}, {"name": "nope"})
        self.assertIn("error", res)


class DispatchWriteTest(unittest.TestCase):
    def _send(self, s, args):
        return pipeline.dispatch(s, {}, {"name": "send_message", "args": args})

    def test_send_appends_and_clears_unread(self):
        s = make_state(unread=5)
        res, sleep = self._send(s, {"bubbles": [{"text": "hi"}, {"text": "all"}]})
        self.assertIsNone(sleep)
        self.assertEqual(res["bubbles"], 2)
        self.assertIn("delivered", res)
        self.assertEqual(s.group[-1]["text"], "hi\nall")
        self.assertEqual(s.unread, 0)

    def test_send_old_string_format_warns(self):
        s = make_state()
        before = len(s.group)
        res, _ = self._send(s, {"text": "hi all"})
        self.assertIn("warning", res)
        self.assertEqual(len(s.group), before)

    def test_send_empty_warns(self):
        s = make_state()
        for args in ({"bubbles": []}, {"bubbles": [{"text": "  "}]}, {"bubbles": "hi"}):
            res, _ = self._send(s, args)
            self.assertIn("warning", res)

    def test_send_over_cap_warns(self):
        s = make_state()
        args = {"bubbles": [{"text": f"m{i}"} for i in range(11)]}
        res, _ = self._send(s, args)
        self.assertIn("warning", res)

    def test_send_cap_boundary_ok(self):
        s = make_state()
        args = {"bubbles": [{"text": f"m{i}"} for i in range(10)]}
        res, _ = self._send(s, args)
        self.assertEqual(res["bubbles"], 10)

    def test_send_reply_to_known_ok(self):
        s = make_state()
        res, _ = self._send(s, {"bubbles": [{"text": "jawab", "reply_to": 1005}]})
        self.assertEqual(res["bubbles"], 1)

    def test_send_reply_to_unknown_warns(self):
        s = make_state()
        before = len(s.group)
        res, _ = self._send(s, {"bubbles": [{"text": "jawab", "reply_to": 999999}]})
        self.assertIn("warning", res)
        self.assertEqual(len(s.group), before)

    def test_send_reply_to_bad_type_warns(self):
        s = make_state()
        res, _ = self._send(s, {"bubbles": [{"text": "x", "reply_to": "1005"}]})
        self.assertIn("warning", res)

    def test_do_activity_freezes(self):
        s = make_state(now_min=100)
        res, sleep = pipeline.dispatch(
            s, {}, {"name": "do_activity", "args": {"label": "sleep", "until": "02:00"}})
        self.assertEqual(sleep, "sleep")
        self.assertGreater(res["sleeping_until"], 100)
        self.assertEqual(s.activity_label, "sleep")


class MemoryTest(unittest.TestCase):
    def test_list_read_write(self):
        s = make_state()
        mems: dict = {}
        res, _ = pipeline.dispatch(
            s, mems, {"name": "memory", "args": {"op": "write", "name": "m1", "text": "hello"}})
        self.assertEqual(res["written"], "m1")
        res, _ = pipeline.dispatch(s, mems, {"name": "memory", "args": {"op": "list"}})
        self.assertEqual(res["files"], ["m1"])
        res, _ = pipeline.dispatch(
            s, mems, {"name": "memory", "args": {"op": "read", "name": "m1"}})
        self.assertEqual(res["text"], "hello")

    def test_rejects_over_1kb(self):
        s = make_state()
        res, _ = pipeline.dispatch(
            s, {}, {"name": "memory",
                    "args": {"op": "write", "name": "a", "text": "x" * 2000}})
        self.assertIn("error", res)

    def test_broken_links_reported(self):
        s = make_state()
        res, _ = pipeline.dispatch(
            s, {}, {"name": "memory",
                    "args": {"op": "write", "name": "m1", "text": "see [[ghost]]"}})
        self.assertEqual(res["broken"], ["ghost"])

    def test_read_missing(self):
        s = make_state()
        res, _ = pipeline.dispatch(
            s, {}, {"name": "memory", "args": {"op": "read", "name": "nope"}})
        self.assertIn("error", res)


class StateMathTest(unittest.TestCase):
    def test_stamina_clamped(self):
        s = make_state(stamina=10)
        apply_stamina(s, 0, "idle", 0, 0, asleep_min=1000)
        self.assertEqual(s.stamina, config.STAMINA_MAX)
        s.stamina = 5
        apply_stamina(s, 600, "active", 600, 10)
        self.assertEqual(s.stamina, 0.0)

    def test_mood_glides(self):
        new = next_mood(5, 500, 2.0, 2.0)
        self.assertGreater(new, 5)
        self.assertLessEqual(abs(new - 5), 3)  # glide, never teleport
        self.assertGreaterEqual(next_mood(0, 0, -2.0, -2.0), 0)

    def test_rel_decay_idle_only(self):
        self.assertEqual(rel_decay(100, 2), 100)
        self.assertLess(rel_decay(100, 10), 100)
        self.assertGreater(rel_decay(-100, 10), -100)

    def test_rel_bands_cover_range(self):
        for score in (-500, -20, 0, 20, 500):
            self.assertTrue(pipeline.rel_band(score))


class WindowAppendTest(unittest.TestCase):
    def _pair(self, tag):
        call = {"id": f"c{tag}", "name": "read_chat", "args": {}}
        return (
            {"role": "assistant", "content": None, "tool_calls": [{
                "id": f"c{tag}", "type": "function",
                "function": {"name": "read_chat", "arguments": "{}"}}]},
            {"role": "tool", "tool_call_id": f"c{tag}",
             "content": '{"x": "%s"}' % tag},
        )

    def test_pinned_lore_never_slides(self):
        s = make_state()
        lore = pipeline.pinned_lore("lore")
        pairs = []
        for i in range(40):
            pairs.extend(self._pair(i))
        s.history = [lore, *pairs]
        pipeline.slide_window(s)
        self.assertIs(s.history[0], lore)
        self.assertEqual(len(s.history), 1 + 2 * config.MAX_PAIRS)

    def test_window_keeps_newest_20_pairs(self):
        s = make_state()
        lore = pipeline.pinned_lore("lore")
        pairs = []
        for i in range(25):
            pairs.extend(self._pair(i))
        s.history = [lore, *pairs]
        pipeline.slide_window(s)
        self.assertIs(s.history[0], lore)
        self.assertEqual(len(s.history), 1 + 2 * config.MAX_PAIRS)
        self.assertEqual(s.history[-2]["tool_calls"][0]["id"], "c24")

    def test_window_untouched_under_cap(self):
        s = make_state()
        lore = pipeline.pinned_lore("lore")
        pairs = []
        for i in range(5):
            pairs.extend(self._pair(i))
        s.history = [lore, *pairs]
        pipeline.slide_window(s)
        self.assertEqual(len(s.history), 1 + 10)

    def test_append_pair_keeps_id_pairing(self):
        s = make_state()
        call = {"id": "call_1", "name": "read_chat", "args": {}}
        pipeline.append_pair(s, call, {"chats": []})
        assistant, tool = s.history[-2], s.history[-1]
        self.assertIsNone(assistant["content"])
        self.assertEqual(assistant["tool_calls"][0]["id"], "call_1")
        self.assertEqual(tool["tool_call_id"], "call_1")


if __name__ == "__main__":
    unittest.main()
