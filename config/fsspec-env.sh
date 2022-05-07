#!/bin/bash

FSSPEC_CONFIG_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]:-$0}")")"
AWS_ACCESS_KEY_ID=$(kubectl get secret --namespace default minio -o jsonpath="{.data.root-user}" | base64 --decode)
AWS_SECRET_ACCESS_KEY=$(kubectl get secret --namespace default minio -o jsonpath="{.data.root-password}" | base64 --decode)

export FSSPEC_CONFIG_DIR
export AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY
