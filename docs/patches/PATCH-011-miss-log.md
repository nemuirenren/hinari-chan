# PATCH-011 — dynamic miss log line

> Date: 2026-09-16. Artifacts `docs/archived_artefact/` are frozen and untouched.

## What changed and why

The idle-sleep log line was a hardcoded `"miss x2, idle sleep"`, so it lied
whenever `MISS_MAX` / `MISS_SLEEP_MIN` differed — including the owner's own
tuning in `config.py` (left untouched by design). The line now reads both
constants, so the log always states the real discipline.

## Files

- Edited: `hinari/main.py` (one log line).
- This doc.

## Verification

- Unit tests green. Owner's `config.py` values verified untouched.
