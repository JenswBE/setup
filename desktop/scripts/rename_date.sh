#!/usr/bin/env bash

# Author: Jens Willemsens <jens@jensw.be>
# License: MIT
#
# === Purpose ===
# Renames media files accordingly to the EXIF or modification date
#
# === Dependencies ===
# - jhead

# Settings
PREFIX="${1}"
APPENDIX="${2}"
OTHER_EXT=("png" "mp4")

# Rename JPEG accordingly to EXIF
jhead -autorot -nf"${PREFIX}%Y-%m-%d_%H-%M-%S_%03i${APPENDIX}" *.jpg *.jpeg

# Rename other files accordingly to modify date
for ext in "${OTHER_EXT[@]}"; do
  for file in *.${ext}; do
    NEW_FILENAME=$(stat "${file}" --format %y | cut -c -19 | tr : - | tr ' ' _)
    mv "${file}" "${PREFIX}${NEW_FILENAME}${APPENDIX}.${ext}"
  done
done
