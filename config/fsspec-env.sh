#!/bin/bash

FSSPEC_CONFIG_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]:-$0}")")"

export FSSPEC_CONFIG_DIR
export AWS_ACCESS_KEY_ID=minioadmin
export AWS_SECRET_ACCESS_KEY=minioadmin
