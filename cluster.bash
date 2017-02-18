#!/usr/bin/env bash

set -euo pipefail
IFS=' '

CLIENT_PORT=${ETCD_CLIENT_PORT:-2379}
SERVER_PORT=${ETCD_SERVER_PORT:-2380}

# Retry N times before giving up
RETRY_TIMES=${RETRY_TIMES:-10}

# Add a sleep time to allow etcd client requets to finish
WAIT_TIME=3
