# PATCH-007 — system-level systemd service

> Date: 2026-09-16. Artifacts `docs/archived_artefact/` are frozen and untouched.
> Owner intent; no YAGNI applied to the what, only to the how.

## What changed and why

The service lived at user level (`~/.config/systemd/user/`), so every command
needed `--user`, it died on logout without linger, and the pattern does not
transfer to a VPS. It now lives at system level (`/etc/systemd/system/`):
plain `systemctl ... hinari` everywhere, on both machines.

## Design

- `./startup.sh --install-service` asks for the sudo password and writes the
  unit, then `daemon-reload` + `enable --now`. No flag still runs foreground.
- The unit sets `User=`/`Group=` to the invoking user (`$SUDO_USER`), so
  `state/`, `log.txt`, and `.env` stay owned by the owner — never root.
- Absolute `WorkingDirectory` (repo root) and absolute `ExecStart` (`uv`
  resolved at install time). Config still comes from `./.env` via code, so no
  `EnvironmentFile` is needed. `WantedBy=multi-user.target`.
- The installer disables and removes the legacy user-level unit first, so two
  bots can never run at once.
- `reset.sh` stops `hinari` via system `systemctl` (sudo) instead of `--user`.
- Day-to-day: `systemctl status|start|stop|restart|disable hinari`;
  `journalctl -u hinari -f` for system logs next to `./log.txt`.

## Files

- Rewrote: `startup.sh`, `reset.sh`.
- This doc.

## Verification

- `bash -n` passes on both scripts; unit content reviewed field by field.
  (Service install itself runs on the owner's machine/VPS, not here.)
