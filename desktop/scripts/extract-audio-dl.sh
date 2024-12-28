#!/bin/bash

# Author: Jens Willemsens <jens@jensw.be>
# License: MIT
#
# === Purpose ===
# Downloads video with YT-DLP and extracts audio into Ogg Opus format
#
# === Dependencies ===
# - yt-dlp
# - ffmpeg / avconv
#
# === Optional ===
# --audio-format mp3: Forces the output to mp3
yt-dlp --ignore-errors --format bestaudio --extract-audio $@
