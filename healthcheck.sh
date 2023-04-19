#!/bin/sh
set -e
DIR='/data/"$RCLONE_MOUNT_NAME"/movies'
if [[ -n -d "$DIR" ]]; then
  exit 1
fi  