#!/bin/bash

# Bash strict mode (http://redsymbol.net/articles/unofficial-bash-strict-mode/)
set -euo pipefail

# Update Docker containers
cd '{{ ansible_facts["user_dir"] }}/deploy'
echo "=== docker compose pull ==="
ec_pull=0;  docker compose --progress plain --profile 'scheduled' pull         || ec_pull=$?
echo "=== docker compose build ==="
ec_build=0; docker compose --progress plain --profile 'scheduled' build --pull || ec_build=$?
echo "=== docker compose up ==="
ec_up=0;    docker compose --progress plain up -d                              || ec_up=$?

# Prune unused Docker resources
echo "=== docker image prune ==="
ec_image_prune=0;  docker image prune -f  || ec_image_prune=$?
echo "=== docker buildx prune ==="
ec_buildx_prune=0; docker buildx prune -f || ec_buildx_prune=$?

# Print overview
cat << EOF

=== Exit codes overview ===
docker compose pull: $ec_pull
docker compose build: $ec_build
docker compose up: $ec_up
docker image prune: $ec_image_prune
docker buildx prune: $ec_buildx_prune
EOF

# Exit with 1 if any step failed
exit $(( ec_pull != 0 || ec_build != 0 || ec_up != 0 || ec_image_prune != 0 || ec_buildx_prune != 0 ))
