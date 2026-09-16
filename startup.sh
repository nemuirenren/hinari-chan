#!/usr/bin/env bash
# Hinari launcher. Usage:
#   ./startup.sh                    # run in foreground
#   ./startup.sh --install-service  # install system service (asks for sudo password)
set -euo pipefail
cd "$(dirname "$0")"

SERVICE=hinari
UNIT=/etc/systemd/system/$SERVICE.service

if [ "${1:-}" = "--install-service" ]; then
  OWNER="${SUDO_USER:-$(id -un)}"
  OWNER_HOME="$(eval echo "~$OWNER")"
  OWNER_GROUP="$(id -gn "$OWNER")"
  UV="$(command -v uv)"

  # Remove the legacy user-level unit so two bots never run at once.
  systemctl --user disable --now "$SERVICE.service" 2>/dev/null || true
  rm -f "$OWNER_HOME/.config/systemd/user/$SERVICE.service"

  echo "Installing $UNIT (sudo password may be asked)..."
  sudo tee "$UNIT" > /dev/null <<EOF
[Unit]
Description=Hinari Discord bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$OWNER
Group=$OWNER_GROUP
WorkingDirectory=$(pwd)
ExecStart=$UV run hinari
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
  sudo systemctl daemon-reload
  sudo systemctl enable --now "$SERVICE.service"
  echo "installed. Manage with: systemctl status|start|stop|restart|disable $SERVICE"
  echo "System logs: journalctl -u $SERVICE -f (bot log stays in ./log.txt)"
  exit 0
fi

exec uv run hinari
