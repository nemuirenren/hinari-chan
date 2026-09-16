# PATCH-014 — reply trigger, burst 6, descriptive group slot

> Date: 2026-09-16. Artifacts `docs/archived_artefact/` are frozen and untouched.
> Owner intent; no YAGNI applied to the what, only to the how.

## What changed and why

Three linked items. Replies to Hinari's bubbles woke nothing (ordinary
chatter); the burst gate sat at 20; and the `<group>` slot text predated the
`replied` flag it now must explain.

## Design

- **Reply trigger.** A message whose `reply_to` quotes one of Hinari's own
  recorded bubbles sets `replied=True`, which interrupts sleep exactly like a
  mention. Self-echoes can't trigger (own messages return before the check).
  The flag rides `group_meta` (`replied=True/False`), persists across
  restarts, and resets at wake close. Old snapshots default it to `False`.
- **Burst 6.** `BURST_THRESHOLD = 20` → `6`. Below it, counts wait for the
  next natural wake.
- **Descriptive `<group>` (owner-authorized section).** Defines all three
  terms, states texts are absent, names the open action, permits silence —
  against hallucinated replies and forced responsiveness. Rest of `SYSTEM.md`
  untouched (owner's file).

## Files

- Edited: `hinari/config.py`, `hinari/harness/state.py`,
  `hinari/harness/pipeline.py` (`is_reply_to_own`), `hinari/main.py`
  (event check, meta string, persist, reset, wake log), `prompts/SYSTEM.md`
  (`<group>` only), `tests/test_harness.py`.
- This doc.

## Verification

- Unit tests green (burst 6/5 boundary, reply interrupt, own/other/unknown
  reply resolution).
- Live boot: login, wake cycle, persist.
