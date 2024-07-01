# This script is intended to be sourced like "source lint.sh" or ". lint.sh".
# Config is available at https://raw.githubusercontent.com/JenswBE/setup/main/programming_configs/golang/.golangci.yml
golangci-lint run \
    -c ../../../../setup/programming_configs/golang/.golangci.yml \
    --disable err113,noctx
