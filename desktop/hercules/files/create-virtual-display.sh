#!/bin/bash
set -euo pipefail

# === CONFIG ===
# Based on https://feddit.org/post/12000513
# Find display port name with:
# for p in /sys/class/drm/*/status; do con=${p%/status}; echo -n "${con#*/card?-}: "; cat $p; done
DISPLAY_PORT="DP-1"
EDID_PATH="/usr/local/lib/firmware/edid-dell-g2724d.bin"

# === SCRIPT ===
DISPLAY_PORT_PATH="/sys/kernel/debug/dri/0/${DISPLAY_PORT}"
cat "${EDID_PATH}" > "${DISPLAY_PORT_PATH}/edid_override"
echo 'on' > "${DISPLAY_PORT_PATH}/force"
echo '1' > "${DISPLAY_PORT_PATH}/trigger_hotplug"
