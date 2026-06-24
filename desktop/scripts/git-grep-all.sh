#!/usr/bin/env bash
# Based on https://stackoverflow.com/a/15293283
mapfile -t commits < <(git rev-list --all)
git grep "$*" "${commits[@]}"
