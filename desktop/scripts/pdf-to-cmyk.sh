#!/usr/bin/env bash
set -euo pipefail

# Based on https://stackoverflow.com/a/8567524

# Params
INPUT_FILE=${1:?An input file is mandatory as first positional parameter}

# Script
BASE_NAME=${INPUT_FILE%.pdf}
OUTPUT_FILE="${BASE_NAME}_CMYK.pdf"
gs \
    -o "${OUTPUT_FILE}" \
    -sDEVICE=pdfwrite \
    -sProcessColorModel=DeviceCMYK \
    -sColorConversionStrategy=CMYK \
    -sColorConversionStrategyForImages=CMYK \
    -dEncodeColorImages=false \
    "${INPUT_FILE}"
