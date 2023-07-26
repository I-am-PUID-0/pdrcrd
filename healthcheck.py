from base import *


def check_plex_debrid():
    try:
        process = "python ./plex_debrid/main.py --config-dir /config"
        subprocess.check_output(f"pgrep -f '{process}'", shell=True)
        return True
    except subprocess.CalledProcessError:
        return False

try:
    if not (os.getenv("RD_API_KEY") is None):
        rclone_mount_name = os.getenv('RCLONE_MOUNT_NAME')
        if rclone_mount_name:
            DIR = f'/data/{rclone_mount_name}/movies'
            if  os.path.isdir(DIR):
                pass
            else:
                raise Exception("The rclone mount is not accessible")

    if not (os.getenv("PLEX_USER") is None):
        if check_plex_debrid():
            pass
        else:
            raise Exception("The plex_debrid process is not running.")

except Exception as e:
    print(str(e), file=sys.stderr)
    exit(1)