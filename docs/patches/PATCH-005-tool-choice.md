# PATCH-005 — tool_choice default auto, one env var

> Date: 2026-09-16. Artifacts `docs/archived_artefact/` are frozen and untouched.
> Owner intent; no YAGNI applied to the what, only to the how.

## What changed and why

`tool_choice: required` pressures the model into calling tools on every turn.
The owner prefers the looser `auto` as the default while keeping an override.

## Design

- **Default `auto` in code.** `call_llm` tries the configured value first and
  falls back to the other one (`auto <-> required`) on failure — the mirror of
  the previous direction.
- **One env var: `TOOL_CHOICE`.** Optional; empty or missing means `auto`.
  Only `auto`/`required` are accepted, anything else fails boot with a clear
  error before any network. The single value drives Hinari, heart, **and**
  compat probes (the tools-less dangling probe is unaffected by construction).
- **`.env` ships `TOOL_CHOICE=auto`; `.env.example` shows the same.**
- **Accepted trade-off.** With `auto` the model may answer in plain text, so
  the miss handler (retry once, then 5-minute idle sleep) fires more often and
  Hinari goes quieter. Miss/warning discipline is otherwise unchanged.
- **Deviation note.** LLD section 5 preferred `required` where supported; this
  patch deliberately inverts the default. Recorded here, artifact untouched.

## Files

- Edited: `hinari/config.py` (parse + validate), `hinari/adapters/llm.py`
  (default + mirrored fallback), `hinari/compat.py` (configured value in
  probes), `hinari/main.py` (pass-through), `.env`, `.env.example`,
  `tests/test_adapters.py`, `tests/test_startup.py`.
- This doc.

## Verification

- Unit tests green (default auto, `Required` normalized, bogus rejected,
  auto->required fallback order, configured value reaching probes).
- Live compat 4/4 with the env value. Live boot: login, wake, persist.
