# PATCH-006 — reply_to, message_id, readable time

> Date: 2026-09-16. Artifacts `docs/archived_artefact/` are frozen and untouched.
> Owner intent; no YAGNI applied to the what, only to the how.

## What changed and why

Three linked upgrades so Hinari reads and answers like a chat native: targeted
replies, quotable message ids, and human-readable timestamps.

## Design

- **Reply per bubble.** Items are `{text, reply_to?}` where `reply_to` is an
  optional Discord `message_id` from the room. Sent via per-bubble
  `MessageReference` (`fail_if_not_exists=False`), so Discord renders the
  quoted original above her bubble. Unknown/outside-room ids and non-integer
  ids return a paired WARNING (Patch-004 philosophy): Discord untouched, state
  untouched, retry unlimited. Replies count toward the 10-bubble cap.
- **`message_id` everywhere it matters.** Group entries carry the Discord id
  (events, backfill, and own sends via the first returned id — multi-bubble
  own calls keep one entry, a recorded v0 limitation). Read/scroll/search
  bubbles expose `{message_id, from, now, text, rel}`. Search hits carry both
  `n` (positional pick index, LLD semantics unchanged) and `message_id`
  (for `reply_to`); `pick` stays index-based, nothing silently redefined.
- **Readable time.** Bubble outputs replace the blind epoch-minute `time`
  with `now` in the exact system format (`Tue, 2026-09-16, 04:20 +0700`,
  local). Epoch minutes stay internal-only for ordering. Scope is bubble
  outputs; memory results and `{delivered}` are untouched.

## Files

- Edited: `hinari/harness/pipeline.py` (`_clean_bubbles`, `_annotate`,
  `format_now`, search hits), `hinari/adapters/llm.py` (schema),
  `hinari/adapters/discord_phone.py` (`send_bubbles` takes items, returns
  ids), `hinari/main.py` (validate-before-mirror, id patching, event ids),
  `tests/test_harness.py`, `tests/test_adapters.py`.
- This doc.

## Verification

- Unit tests green (ids in outputs, readable `now`, reply known/unknown/bad,
  hits carry `n` + `message_id`, no legacy `id` key).
- Live boot: login, wake cycle, persist.
