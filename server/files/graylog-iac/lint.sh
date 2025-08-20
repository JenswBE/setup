# This script is intended to be sourced like "source lint.sh" or ". lint.sh".
golangci-lint run --config ../../../programming_configs/golang/.golangci.yml --path-prefix "files/graylog-iac"
