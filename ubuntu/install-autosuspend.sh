#!/usr/bin/env bash
# Install autosuspend with the adjacent config. Run: sudo ./install-autosuspend.sh
set -euo pipefail
cd "$(dirname "$0")"

[ "$(id -u)" -eq 0 ] || { echo "run me with sudo" >&2; exit 1; }

# Mask before installing: the package's postinst starts the daemon straight
# away using the shipped example config (15 min idle, pings a host that does
# not exist on this LAN), which would suspend this machine mid-session.
systemctl mask autosuspend.service

apt-get install -y autosuspend

install -m 0755 gpu-busy       /usr/local/bin/autosuspend-gpu-busy
install -m 0644 autosuspend.conf /etc/autosuspend.conf

systemctl unmask autosuspend.service
systemctl enable --now autosuspend.service autosuspend-detect-suspend.service

systemctl --no-pager --full status autosuspend.service || true
