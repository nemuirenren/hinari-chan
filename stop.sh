#!/usr/bin/env bash
# Stop the Hinari service.
set -euo pipefail

sudo systemctl stop hinari
echo "hinari stopped (status: systemctl status hinari)"
