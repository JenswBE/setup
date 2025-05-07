#!/usr/bin/env bash

# Bash strict mode (http://redsymbol.net/articles/unofficial-bash-strict-mode/)
set -euo pipefail

# Set SSH port
SSH_PORT=8477
echo ">> Updating SSH port to ${SSH_PORT}"
echo "set /files/etc/ssh/sshd_config/Port ${SSH_PORT}" | augtool -s 1> /dev/null

# Setup authorized_keys files
USERS=$(echo $SSH_USERS | tr "," "\n")
for U in $USERS; do
    IFS=':' read -ra UA <<< "$U"
    _NAME=${UA[0]}
    _UID=${UA[1]}
    _GID=${UA[2]}
    _SSH_KEY_SOURCE="/keys_to_authorize/${_NAME}"
    _SSH_KEY_TARGET="/etc/authorized_keys/${_NAME}"

    echo ">> Configuring SSH key for user ${_NAME} in path ${_SSH_KEY_TARGET}."
    echo -n "command=\"/usr/bin/rrsync /data/${_NAME}\" " > "${_SSH_KEY_TARGET}"
    cat "${_SSH_KEY_SOURCE}" >> "${_SSH_KEY_TARGET}"
    chown ${_UID}:${_GID} "${_SSH_KEY_TARGET}"
done

# Correct permissions of /etc/entrypoint.d
chmod 755 /etc/entrypoint.d/*

# Cleanup
rm -rf /keys_to_authorize
