#!/bin/bash

# Source cargo env
. ~/.cargo/env

# Ensure we are at latest main
git switch main
git pull

# Create new branch
git switch -c bump-deps

# Update cargo.lock
cargo update

# Commit changes
git add -A
git commit -m "Bump deps"

# Push branch
git push -u origin bump-deps

# Checkout main
git switch main

# Remove bump-deps branch locally
git branch -D bump-deps
