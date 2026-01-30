#!/bin/bash
# Error logic based on https://stackoverflow.com/a/44708091

# Bash strict mode (http://redsymbol.net/articles/unofficial-bash-strict-mode/)
set -euo pipefail

# Update Docker containers
cd '{{ ansible_user_dir }}/deploy'
docker compose --profile 'scheduled' pull || exit_status=1
docker compose --profile 'scheduled' build --pull || exit_status=1
docker compose up -d || exit_status=1

# Prune unused Docker resources
docker image prune -f || exit_status=1
docker buildx prune -f || exit_status=1

# Exit with status
exit ${exit_status:-0}
