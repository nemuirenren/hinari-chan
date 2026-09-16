#!/usr/bin/env bash
# Factory reset: wipe runtime state only. Prompts and .env are kept.
set -euo pipefail
cd "$(dirname "$0")"

sudo systemctl stop hinari 2>/dev/null || true
rm -rf state log.txt
mkdir -p state
echo "reset done: state/ and log.txt cleared"
