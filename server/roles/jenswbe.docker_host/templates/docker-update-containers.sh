#!/bin/bash
# Error logic based on https://stackoverflow.com/a/44708091

# Bash strict mode (http://redsymbol.net/articles/unofficial-bash-strict-mode/)
set -euo pipefail

# Update Docker containers
cd '{{ ansible_user_dir }}/deploy'
docker compose --profile 'scheduled' pull || update_failed=1
docker compose --profile 'scheduled' build --pull || update_failed=1
docker compose up -d || update_failed=1

if [ ${update_failed:-0} -eq 0 ]
then
    echo "Update successful. Pruning unused images ..."
    docker image prune -f
    docker buildx prune -f
else
    echo "Update failed. Please check"
fi
