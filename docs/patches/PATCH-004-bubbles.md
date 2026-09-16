# PATCH-004 — send_message bubbles array

> Date: 2026-09-16. Artifacts `docs/archived_artefact/` are frozen and untouched.
> Owner intent; no YAGNI applied to the what, only to the how.

## What changed and why

The `\n\n`-split convention for multi-bubble chat is retired: string splitting
is invisible magic the model must guess. `send_message` now takes an explicit
array of bubble objects, so one bubble is one declared item. Bubble count per
call is hers to choose, capped at 10 for channel safety.

## Design

- **Schema.** `send_message({bubbles: [{text}, ...]})`. Non-empty array only;
  whitespace-only texts are dropped; zero survivors is invalid. Max 10 per
  call (Discord rate limits absorb this; `discord.py` sleeps on 429).
- **Validation warnings (unlimited retry).** Any format violation returns a
  `{"warning": ...}` tool result paired with her call id — Discord untouched,
  no state touched. The warning is appended to history, so she reads her own
  correction next iteration and retries. No miss-counter cutoff applies here;
  the only backstop is the per-wake tool-loop ceiling, and she may continue
  next wake. Transport failure (0 bubbles delivered) keeps returning
  `{"error": "send failed"}`; partial delivery notes `{partial: true, sent}`.
- **Storage.** One group entry per call, texts joined with a single newline.
  `\n\n` appears nowhere in input or storage anymore, so the model can never
  re-learn the old convention from her own history.
- **Typing.** Unchanged: per-bubble typing indicator plus
  `min(len * 0.02s, 5s)` delay; the exact curve stays deferred per LLD 10.

## Files

- Edited: `hinari/adapters/llm.py` (schema), `hinari/config.py` (`MAX_BUBBLES`),
  `hinari/harness/pipeline.py` (`_clean_bubbles` + dispatch), 
  `hinari/adapters/discord_phone.py` (`send_bubbles` takes a list),
  `hinari/main.py` (validate-before-mirror + partial note),
  `tests/test_harness.py`, `tests/test_adapters.py`.
- This doc.

## Verification

- Unit tests green, including old-string-format warns, empty warns,
  over-cap warns, and the 10-boundary pass.
- Live boot: login, wake cycle, persist.
