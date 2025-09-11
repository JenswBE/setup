#!/bin/bash

# This script overlays the public and private setup repo's

set -euo pipefail

# PARAMS
base_dir=$(realpath ${PWD}/../..)
lower_dirs="$(pwd):${base_dir}/setup-private/server"
merged_dir="${base_dir}/server-merged"

# SCRIPT
sudo umount "${merged_dir}" || true
echo "Lower dirs: ${lower_dirs}"
echo "Merged dir: ${merged_dir}"
mkdir -p ${merged_dir}
sudo mount -t overlay overlay -o lowerdir="${lower_dirs}" "${merged_dir}"
