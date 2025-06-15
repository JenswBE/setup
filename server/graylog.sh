#!/usr/bin/env bash

# Bash strict mode (http://redsymbol.net/articles/unofficial-bash-strict-mode/)
set -euo pipefail

cd files/graylog-iac
go run ./...
