#!/usr/bin/env bash
echo "Setting up cabin-iot-gateway environment"
export PROJECT_DIR=$(git rev-parse --show-toplevel)
source $PROJECT_DIR/.env
