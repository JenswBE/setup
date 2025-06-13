#!/usr/bin/env bash

# Managed by Ansible at server/roles/jenswbe.vm_host/files/clone-vm.sh

# Bash strict mode (http://redsymbol.net/articles/unofficial-bash-strict-mode/)
set -euo pipefail

# Params
VM_FROM="${1:?Script expects VM_FROM as the first positional argument}"
VM_TO="${2:?Script expects VM_FROM as the second positional argument}"

# Helper funcs
function get_vm_state(){
  virsh domstate "${1}" | tr -d '[:space:]'
}

# Init
echo "Cloning VM ${VM_FROM} to ${VM_TO} ..."
VM_FROM_STATE=$(get_vm_state "${VM_FROM}")
VM_FROM_DISK=$(virsh domblklist ${VM_FROM} | grep -F vda | sed -E 's/.+ //')
POOL_PATH=$(dirname "${VM_FROM_DISK}")
VM_TO_DISK="${POOL_PATH}/${VM_TO}.qcow2"
echo "Input disk:  ${VM_FROM_DISK}"
echo "Output disk: ${VM_TO_DISK}"

# Clone VM
if [[ ${VM_FROM_STATE} == "running" ]]; then
  echo -e "\nShutting down ${VM_FROM} ..."
  virsh shutdown "${VM_FROM}"
  while [[ $(get_vm_state "${VM_FROM}") != "shutoff" ]]; do
    sleep 5s
    echo "Awaiting shutdown of ${VM_FROM} ..."
  done
fi
virt-clone --original "${VM_FROM}" --name "${VM_TO}" --file "${VM_TO_DISK}"
if [[ ${VM_FROM_STATE} == "running" ]]; then
  echo -e "\nRestarting ${VM_FROM} ..."
  virsh start "${VM_FROM}"
fi

# "dpkg-reconfigure openssh-server" is needed on Debian to regenerate the SSH host keys
echo -e "\nReset ${VM_TO} (machine-id, SSH host keys, ...)"
virt-sysprep --domain "${VM_TO}" --hostname "${VM_TO}" --operations defaults,-ssh-userdir --run-command 'dpkg-reconfigure openssh-server'
