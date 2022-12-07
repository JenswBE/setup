#!/bin/bash

# Author: Jens Willemsens <jens@jensw.be>
# License: MIT
#
# === Purpose ===
# Small helper to encrypt a file to <filename>.gpg using AES256. Passphrase is asked at execution.
#
# === Dependencies ===
# - gpg

gpg -c -o "$1.gpg" --cipher-algo AES256 "$1"
