#!/bin/bash

# Author: Jens Willemsens <jens@jensw.be>
# License: MIT
#
# === Purpose ===
# Downloads video with youtube-dl and extracts audio into Ogg Opus format
#
# === Dependencies ===
# - youtube-dl
# - ffmpeg / avconv
#
# === Command ===
# -i: Ignore errors
# -x: Extract audio
# -f bestaudio: Download format with best audio
# --audio-quality 0: Convert to best audio quality
youtube-dl -i -x -f bestaudio --audio-format opus --audio-quality 0 $@
