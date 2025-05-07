#!/usr/bin/env bash

# Bash strict mode (http://redsymbol.net/articles/unofficial-bash-strict-mode/)
set -euo pipefail

# Fix permissions of mounted data volumes
USERS=$(echo $SSH_USERS | tr "," "\n")
for U in $USERS; do
    IFS=':' read -ra UA <<< "$U"
    _NAME=${UA[0]}
    _UID=${UA[1]}
    _GID=${UA[2]}

    echo ">> Chown /data/${_NAME} to user ${_NAME} (${_UID}:${_GID})."
    chown -R ${_UID}:${_GID} "/data/${_NAME}"
done
