#!/usr/bin/env bash

# Managed by Ansible at server/roles/jenswbe.vm_host/files/start-after-nfs.sh

# Bash strict mode (http://redsymbol.net/articles/unofficial-bash-strict-mode/)
set -euo pipefail

# Params
NFS_SERVER="${1:?Script expects NFS_SERVER as the first positional argument}"
VM_TO_START="${2:?Script expects VM_TO_START as the second positional argument}"

# Fix VM name
# SystemD replaces dashes with a slash
VM_TO_START=$(echo "${VM_TO_START}" | tr '/' '-')

# Wait for NFS server
until nc -z "${NFS_SERVER}" 2049
do
    echo "Waiting for NFS server ..."
    sleep 10s
done

# Start VM
echo "NFS is running. Starting VM ..."
virsh start "${VM_TO_START}"
