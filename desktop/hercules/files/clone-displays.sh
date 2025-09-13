#!/bin/bash

set -euo pipefail

# === PARAMS ===
DISPLAY_MODE="1920x1080@60"
VIRT_DISPLAY_NAME="DP-1"
REAL_DISPLAY_NAME="HDMI-A-1"

# === SCRIPT ===
echo "Cloning displays '${VIRT_DISPLAY_NAME}' and '${REAL_DISPLAY_NAME}' with mode '${DISPLAY_MODE}'"
QT_QPA_PLATFORM=wayland kscreen-doctor \
    "output.${VIRT_DISPLAY_NAME}.mode.${DISPLAY_MODE}" \
    "output.${VIRT_DISPLAY_NAME}.enable" \
    "output.${VIRT_DISPLAY_NAME}.priority.1" \
    "output.${REAL_DISPLAY_NAME}.mode.${DISPLAY_MODE}" \
    "output.${REAL_DISPLAY_NAME}.enable" \
    "output.${REAL_DISPLAY_NAME}.priority.2" \
    "output.${REAL_DISPLAY_NAME}.mirror.${VIRT_DISPLAY_NAME}"
