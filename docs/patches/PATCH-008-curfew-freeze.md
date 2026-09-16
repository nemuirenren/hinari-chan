# PATCH-008 — curfew semantics freeze (no behavior change)

> Date: 2026-09-16. Artifacts `docs/archived_artefact/` are frozen and untouched.
> Owner intent; no YAGNI applied to the what, only to the how.

## What changed and why

Investigation (not a behavior bug): the night curfew matched its intent but
two of its semantics lived only in code — an end hour the LLD never states,
and a stamina-full guard the LLD never states. The LLD letter
(">= 01:00 forces sleep until 500") is unimplementable verbatim: with full
stamina at 02:00 it would force-sleep one minute and refire every tick, an
all-night loop. This patch freezes the working semantics and names the
constants. Zero behavior change.

## Frozen semantics

- Curfew fires when `CURFEW_START <= local_hour < CURFEW_END` (01:00–04:59)
  **and** stamina is below max. At 05:00+ normal TRIGGER rules apply
  (`until` / mention / burst / stamina — `force-stamina` still guards zero).
- Full stamina inside the window means no forced sleep: a rested Hinari may
  be awake at 03:00.
- Curfew is evaluated before `until`, so it overrides even her own planned
  sleep, converting it into sleep-until-full.
- Hour follows server local time (LLD 10 timezone binding stays deferred —
  real on a VPS).

## Files

- Edited: `hinari/config.py` (dead `CURFEW_HOUR` replaced by `CURFEW_START`
  / `CURFEW_END`, actually read by code), `hinari/main.py`
  (`curfew_active` reads config, hour injectable for tests),
  `tests/test_smoke.py` (boundary tests).
- This doc.

## Verification

- Unit tests green, including 00:59 off / 01:00 on / 04:59 on / 05:00 off.
