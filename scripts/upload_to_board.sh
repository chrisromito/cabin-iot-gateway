#!/usr/bin/env bash
source ./scripts/env.sh
cd $PROJECT_DIR
rshell --port $RSHELL_PORT rsync src /pyboard
