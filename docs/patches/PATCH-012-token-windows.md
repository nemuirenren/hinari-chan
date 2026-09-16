# PATCH-012 — real token windows (tiktoken, 150k, suffix-minimum)

> Date: 2026-09-16. Artifacts `docs/archived_artefact/` are frozen and untouched.
> Owner intent; no YAGNI applied to the what, only to the how.

## What changed and why

Both windows ran on entry-count stand-ins (31 entries) instead of tokens:
early forgetting on quiet days, over-budget risk on busy ones. Both windows
are now measured with tiktoken (`cl100k_base`, cached): Hinari and heart at
150k each, with no pair-count cap — pairs accumulate freely under budget and
only the minimum oldest suffix is dropped past it.

## Design

- New `hinari/tokens.py`: deterministic JSON serialization per message plus a
  documented ~4-token chatML-ish overhead. Exact only for matching BPE; a
  close approximation on third-party proxies. `tiktoken` added via
  `uv add tiktoken` (0.14.0, light Rust wheel, no heavy deps).
- **Suffix-minimum rule (sole rule).** Pins 0–1 absolute (never dropped, but
  counted). Remaining units chunked in whole pairs from the newest side;
  accumulate newest-first; the first unit breaking budget drops it and all
  older at once. Under budget nothing moves. A lone oversized pair is kept
  whole plus a log warning — pairing integrity beats the budget. Pins alone
  over budget are kept plus a warning.
- `CTX_BUDGET = HEART_BUDGET = 150_000` (enforced). `PROTECT_LAST` deleted
  everywhere including persistence: `harness.json` now stores full histories.
  (Rebuilt per-wake `system` is ~1k uncounted headroom against the pin count;
  negligible at 150k, recorded here.)
- LLD section 7's newest-20 floor is superseded by this rule. Locked
  `test_pipeline.py` pseudocode keeps its old count-based slide (file frozen;
  node names unchanged).

## Files

- New: `hinari/tokens.py`, `tests` additions, this doc.
- Edited: `hinari/config.py`, `hinari/harness/pipeline.py`,
  `hinari/heart.py`, `hinari/main.py` (full-history persist),
  `tests/test_harness.py`, `tests/test_heart.py`, `pyproject.toml`/`uv.lock`.
- Deleted: `PROTECT_LAST`.

## Verification

- Unit tests green (deterministic counts, suffix math, pin safety, oversized
  kept whole, heart suffix).
- Live boot: login, wake cycle, persist (tiktoken live in venv).
