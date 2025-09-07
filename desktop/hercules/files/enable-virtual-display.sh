#!/bin/bash

set -euo pipefail

# === PARAMS ===
VIRT_DISPLAY_WIDTH=${1:?Virtual display width is expected as first positional argument}
VIRT_DISPLAY_HEIGHT=${2:?Virtual display height is expected as second positional argument}
VIRT_DISPLAY_RATE=${3:?Virtual display refresh rate is expected as third positional argument}
VIRT_DISPLAY_NAME="DP-1"
REAL_DISPLAY_NAME="HDMI-A-1"

# === SCRIPT ===
VIRT_DISPLAY_MODE="${VIRT_DISPLAY_WIDTH}x${VIRT_DISPLAY_HEIGHT}@${VIRT_DISPLAY_RATE}"
echo "Enabling virtual display '${VIRT_DISPLAY_NAME}' with mode '${VIRT_DISPLAY_MODE}' and disabling real display '${REAL_DISPLAY_NAME}'"
kd_output=$(kscreen-doctor \
    "output.${VIRT_DISPLAY_NAME}.mode.${VIRT_DISPLAY_MODE}" \
    "output.${VIRT_DISPLAY_NAME}.enable" \
    "output.${REAL_DISPLAY_NAME}.disable")
if [[ "${kd_output}" == *"not found"* ]]; then
  modes=$(kscreen-doctor --outputs | grep -A10 -F HDMI-A-1 | grep -iF modes)
  echo -e "Invalid mode '${VIRT_DISPLAY_MODE}' for '${VIRT_DISPLAY_NAME}'. Supported modes are:\n${modes}"
  exit 1
fi

