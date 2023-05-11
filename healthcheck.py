import os

rclone_mount_name = os.getenv('RCLONE_MOUNT_NAME')
DIR = f'/data/{rclone_mount_name}/movies'

if os.path.isdir(DIR):
    exit(0)