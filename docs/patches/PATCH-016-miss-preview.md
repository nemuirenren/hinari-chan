# PATCH-016 — miss preview in logs

> Date: 2026-09-16. Artifacts `docs/archived_artefact/` are frozen and untouched.
> Owner intent; no YAGNI applied to the what, only to the how.

## What changed and why

Misses were countable but blind: the log said a miss happened without showing
what the model said instead of acting. Each miss now logs one INFO line with
the finish reason plus a bounded content preview, so the owner can see the
shape of tool-less replies.

## Design

- `miss #N finish=<reason> preview=<300 chars>` at INFO, then the existing
  idle line at exhaustion. Empty/None content renders `<empty>`; overlong
  text truncates with a `[+N chars]` remainder marker.
- The preview rides `raw_content` (carried beside normalized `None`), so the
  history invariant is untouched: appended pairs still store `content=None`.
- Sensitivity note: this is the first free model text in `log.txt` (it was
  status-only before). It flows through the existing secret-redact filter;
  treat the log file accordingly.
- One behavior fix folded in: `call_llm` is now passed the configured
  `tool_choice` (it silently used the `auto` default before, so a `required`
  env never reached the model).

## Files

- Edited: `hinari/config.py` (`MISS_PREVIEW`), `hinari/harness/pipeline.py`
  (`normalize` carries `raw_content`, `miss_preview`), `hinari/main.py`
  (finish capture + INFO line + configured tool_choice),
  `tests/test_harness.py`.
- This doc.

## Verification

- Unit tests green (empty/short/truncated previews, miss counting).
- Live boot: login, wake cycle, persist.
