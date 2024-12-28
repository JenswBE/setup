#!/usr/bin/env bash
# Based on https://stackoverflow.com/a/15293283
git grep $* $(git rev-list --all)
