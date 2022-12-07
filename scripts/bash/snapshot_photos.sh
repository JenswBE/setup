#!/bin/bash

# Author: Jens Willemsens <jens@jensw.be>
# License: MIT
#
# === Purpose ===
# For each top directory: Tar contents, compresses with BZIP2 and encrypts with AES256
#
# === Dependencies ===
# - gpg
# - parallel

# Read password
read -sp "Enter Password: " GPGPASS
echo
read -sp "Confirm Password: " GPGPASS2

if [ "${GPGPASS}" != "${GPGPASS2}" ]; then
  echo -e "\nPasswords don't match!"
  exit
fi

# Build GPG arguments
GPGOPT="--cipher-algo AES256 --compress-algo BZIP2 --batch --passphrase ${GPGPASS} -c"

# For each top directory:
# 1. Tar contents
# 2. Compress and encrypt
find . -maxdepth 1 -type d ! -name "." | parallel --eta 'tar c -C {} . | gpg -o {}.tar.bz2.gpg' ${GPGOPT}
