# PATCH-015 — pair-count windows (20/20) + token telemetry

> Date: 2026-09-16. Artifacts `docs/archived_artefact/` are frozen and untouched.
> Owner intent; no YAGNI applied to the what, only to the how.

## What changed and why

Token-limit sliding (Patch-012) is reverted: the owner prefers a plain
newest-N-pairs window. Both agents keep pin 0–1 plus the newest 20 pairs
(42 / 40 entries); older whole pairs drop outright with no token math and no
exceptions. This is, deliberately, LLD section 7's original shape.

## Design

- `config.MAX_PAIRS = 20`, shared by Hinari and heart. `CTX_BUDGET` /
  `HEART_BUDGET` (150k) step down to **warn-only telemetry**: every wake logs
  both window sizes in tokens and warns past budget. Visibility without
  enforcement; tiktoken stays for exactly this job.
- Accepted trade-off (stated openly): quiet days forget early (small pairs
  underuse the budget); storm days can exceed it (then the warning fires and
  the provider decides). No pair is ever halved.
- `PROTECT_LAST` is gone for the second and final time; persistence stores
  full histories again (bounded in practice by the 20-pair slide).

## Files

- Edited: `hinari/config.py`, `hinari/harness/pipeline.py`,
  `hinari/heart.py`, `hinari/main.py` (telemetry),
  `tests/test_harness.py`, `tests/test_heart.py`.
- This doc.

## Verification

- Unit tests green (20-pair keep, untouched under cap, pin safety).
- Live boot: login, wake cycle with token telemetry line, persist.
