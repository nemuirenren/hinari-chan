# PATCH-013 — 240s timeouts everywhere

> Date: 2026-09-16. Artifacts `docs/archived_artefact/` are frozen and untouched.
> Owner intent; no YAGNI applied to the what, only to the how.

## What changed and why

Reasoning-strong models think long; the old 60/90/30s timeouts false-failed
them as incompatible (compat) or as misses (wake, heart). All three call
sites now allow 240 seconds. Numbers only — zero logic change.

## Design

- `config.COMPAT_TIMEOUT = 240` (compat probes, worst-case boot +12 min),
  `config.CALL_TIMEOUT = 240` (main-loop calls, default wired through),
  `config.HEART_TIMEOUT = 240` (was 30; each read can now block the tool
  loop up to 4 minutes).
- Recorded cost: a fully silent wake can park up to 10 x 240s before its
  1-minute idle; read-heavy wakes on slow models run longer still.

## Files

- Edited: `hinari/config.py`, `hinari/adapters/llm.py`,
  `hinari/compat.py`, `tests/test_adapters.py`.
- This doc.

## Verification

- Unit tests green (240 wired into all three paths, fallback intact).
- Live compat + live boot.
