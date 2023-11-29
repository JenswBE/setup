#!/bin/bash

# Ensuring sudo is available before running script
sudo echo -n

# Stop backend to close connections
docker stop bjoetiek-test-backend

# Drop and recreate database
docker exec bjoetiek-test-db dropdb -U bjoetiek-test bjoetiek-test
docker exec bjoetiek-test-db createdb -U bjoetiek-test -T template0 bjoetiek-test

# Copy data from Production
docker exec bjoetiek-db pg_dump -Fc -U bjoetiek bjoetiek | docker exec -i bjoetiek-test-db pg_restore -U bjoetiek-test --no-owner -d bjoetiek-test

# Clone images
sudo rsync --archive --verbose --human-readable --delete "{{ general_path_appdata }}/bjoetiek/backend/images/" "{{ general_path_appdata }}/bjoetiek/backend-test/images/" 

# Start backend again
docker compose up -d bjoetiek-test-backend