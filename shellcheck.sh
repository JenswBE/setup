#!/usr/bin/env bash

find . -name "*.sh" \
    -not -path "*/ansible_collections/*" \
    -not -path "*/templates/*" \
    -print0 | xargs -0 shellcheck
