#!/bin/bash

set -eo pipefail

# === PARAMS ===
VIRT_DISPLAY_WIDTH=${SUNSHINE_CLIENT_WIDTH}
if [ -z "${VIRT_DISPLAY_WIDTH}" ]; then
  VIRT_DISPLAY_WIDTH=${1:?Virtual display width is expected as env var SUNSHINE_CLIENT_WIDTH or first positional argument}
fi
VIRT_DISPLAY_HEIGHT=${SUNSHINE_CLIENT_HEIGHT}
if [ -z "${VIRT_DISPLAY_HEIGHT}" ]; then
  VIRT_DISPLAY_HEIGHT=${2:?Virtual display height is expected as env var SUNSHINE_CLIENT_HEIGHT or second positional argument}
fi
VIRT_DISPLAY_RATE=${SUNSHINE_CLIENT_FPS}
if [ -z "${VIRT_DISPLAY_RATE}" ]; then
  VIRT_DISPLAY_RATE=${3:?Virtual display height is expected as env var SUNSHINE_CLIENT_FPS or third positional argument}
fi
VIRT_DISPLAY_NAME="DP-1"
REAL_DISPLAY_NAME="HDMI-A-1"

# === SCRIPT ===
set -u
VIRT_DISPLAY_MODE="${VIRT_DISPLAY_WIDTH}x${VIRT_DISPLAY_HEIGHT}@${VIRT_DISPLAY_RATE}"
echo "Enabling virtual display '${VIRT_DISPLAY_NAME}' with mode '${VIRT_DISPLAY_MODE}' and disabling real display '${REAL_DISPLAY_NAME}'"
kd_output=$(QT_QPA_PLATFORM=wayland kscreen-doctor \
    "output.${REAL_DISPLAY_NAME}.disable" \
    "output.${VIRT_DISPLAY_NAME}.mode.${VIRT_DISPLAY_MODE}" \
    "output.${VIRT_DISPLAY_NAME}.enable")
if [[ "${kd_output}" == *"not found"* ]]; then
  modes=$(QT_QPA_PLATFORM=wayland kscreen-doctor --outputs | grep -A10 -F ${VIRT_DISPLAY_NAME} | grep -iF modes)
  echo -e "Invalid mode '${VIRT_DISPLAY_MODE}' for '${VIRT_DISPLAY_NAME}'. Supported modes are:\n${modes}"
  echo "Reverting to cloned displays ..."
  /usr/local/bin/clone-displays.sh
  exit 1
fi
