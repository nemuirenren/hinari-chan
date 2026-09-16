# PATCH-009 — inbound reply context

> Date: 2026-09-16. Artifacts `docs/archived_artefact/` are frozen and untouched.
> Owner intent; no YAGNI applied to the what, only to the how.

## What changed and why

When someone replied to Hinari's bubble, she saw bare text with no link to
what it answered ("setuju!" answering what?). Discord keeps the quote in the
message `reference`, which we never stored. Now she sees it.

## Design

- **Capture.** `on_message` stores `reply_to` (referenced id) plus `quoted`
  (referenced text): cache-resolved first, one best-effort fetch when the
  target sits outside the cache, silently `None` on failure. Backfill uses
  resolved-only (no per-message fetch storms).
- **Exposure.** Read/scroll/search bubbles always carry `reply_to`/`quoted`
  (`None` when not a reply — explicit shape, no guessing). Heart batches
  render the quote inline (`[replying to '...']`) so tone judgments keep
  their target.
- **Scope.** Presentation only: no TRIGGER change, no new tools, no state
  math change. Old snapshots without the keys load fine via defaults.

## Files

- Edited: `hinari/adapters/discord_phone.py` (`note_message` fields),
  `hinari/main.py` (event capture, backfill mapping, heart batch),
  `hinari/harness/pipeline.py` (`_annotate` shape),
  `tests/test_harness.py`, `tests/test_adapters.py`.
- This doc.

## Verification

- Unit tests green (reply shown with quote, non-replies explicit `None`,
  buffer dedup keeps refs).
- Live boot: login, wake cycle, persist.
