# PATCH-010 — miss patience 10x, idle 1 minute

> Date: 2026-09-16. Artifacts `docs/archived_artefact/` are frozen and untouched.
> Owner intent; no YAGNI applied to the what, only to the how.

## What changed and why

Hinari gave up after 2 tool-less answers and idled 5 minutes. The owner wants
more patience per wake and a shorter nap: up to 10 consecutive misses on the
same snapshot, then 1 idle minute. Scope is Hinari's main loop only — heart
keeps its own discipline (one warned retry, then fail-open, never sleeps).

## Design

- `MISS_MAX = 10`, `MISS_SLEEP_MIN = 1` in `config.py`; `handle_miss` retries
  while below max, then idles and resets. Misses still append nothing, ever.
- Accepted trade-off: a silent wake can now burn up to 10 LLM calls (cost +
  latency) before idling. Under `auto` tool choice this buys plain-text-prone
  models 10 chances to pick up a tool per wake.
- Deviation note: LLD section 5 / invariant 4 say retry-once then 5 minutes.
  Recorded here; artifact untouched; locked `test_pipeline.py` pseudocode
  untouched.

## Files

- Edited: `hinari/config.py`, `hinari/harness/pipeline.py`,
  `tests/test_harness.py`.
- This doc.

## Verification

- Unit tests green (9x retry, 10th sleeps 1 min, counter resets).
- Live boot: login, wake cycle, persist.
