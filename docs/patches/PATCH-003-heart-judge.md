# PATCH-003 — Heart Judge (background)

> Date: 2026-09-16. Artifacts `docs/archived_artefact/` are frozen and untouched.
> Owner intent; no YAGNI applied to the what, only to the how.

## What changed and why

Hinari's relationship engine was purely structural (replies, mentions, ignores).
It could not tell a warm tease from a cold insult, because tone was never read —
sentiment classifiers were a v0 non-goal, and they still are. Instead, a second
agent, **heart**, judges how words land on Hinari and folds the verdict into the
same state the old engine used. The old structural gain/loss path is deleted.

## Design

- **Position.** Heart is a harness function, not Hinari's tool and never in her
  history. It runs synchronously after each read-path DISPATCH (`read_chat`,
  `scroll_chat`, `search_chat`, `memory.read`), before state update. Fail-open:
  any failure means no change, and the tool loop continues.
- **Prompt stack (mirrors Hinari).** `[0] system` from owner-editable
  `prompts/HEART.md` · `[1] assistant` pinned `{identity}` verbatim from
  `IDENTITY.md` (never slides, never normalized) · `[2+]` heart's own judgment
  history under a 50k sliding window. One `IDENTITY.md` serves both agents.
- **Tool, not JSON-in-content.** Heart must call `update_feelings(assessments:
  [{sender, warmth, rel_delta, reason}])`. Tool arguments are protocol-enforced
  valid JSON; free-text content is not (research E3/E4). An empty list is a
  valid deliberate neutral verdict.
- **Miss discipline (non-negotiable).** No tool call, or malformed arguments,
  comes back as a `tool`-role WARNING carrying the `update_feelings` id (the
  call's own id when one exists, the constant otherwise) — never written into
  heart's system (E4: dangling ids are presence-validated). Retry once on the
  same snapshot, then fail-open with nothing appended anywhere.
- **Parameters.** Temperature `0.4`, same model as Hinari, no separate env,
  30s timeout.
- **Bounds (asymmetric by design).** `warmth` -4..+2 per call. `rel_delta`
  -30..+5 per call. Upside capped at +8 per sender per day; downside uncapped.
  Scores clamp to -500..+500; the 13 bands are unchanged.
- **Folding (no new equations).** `rel = clamp(score + delta)`.
  `social_part = mean((rel/500)*2 + warmth)` over assessed senders, then the
  unchanged momentum formula. Unknown senders start Neutral. Decay past 3 idle
  days is kept (time-based, not treatment-based).
- **SYSTEM.md full-template.** The renderer substitutes the whole owner file:
  every byte is kept, placeholders replaced, future XML tags pass through.
  Slot values remain counts/flags (trust boundary).

## Files

- New: `hinari/heart.py`, `prompts/HEART.md`, `tests/test_heart.py`, this doc.
- Edited: `hinari/main.py` (template render, heart hookup, structural removal),
  `hinari/harness/pipeline.py` (template renderer), `hinari/adapters/llm.py`
  (tool/temperature overrides for heart), `hinari/config.py` (heart constants),
  `hinari/compat.py` (probe 4: dangling tool id must not 400),
  `tests/test_harness.py`, `tests/test_startup.py`, `tests/test_smoke.py`.
- Moved: LLD + Blueprint into `docs/archived_artefact/` (frozen).

## Verification

- 75 stdlib unit tests green (locked `test_pipeline.py` untouched).
- Live compat: 4 probes pass (basic call, closed loop, robustness, dangling id).
- Live boot: Discord login, wake cycle with heart judgments, miss path, persist.

## Note (added later)

`docs/pipeline.png` (the 13-node visual) was moved to `docs/archived_artefact/pipeline.png`
with the other frozen artifacts. References to the old path in the locked LLD
(`docs/result/pipeline.png`, itself already stale) are left as-is: artifacts
are never edited.
