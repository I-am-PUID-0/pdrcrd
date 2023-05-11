from base import *


process_name = "python /plex_debrid/main.py --config-dir /config"
def check_plex_debrid():
    try:
        subprocess.check_output(f"pgrep -f '{process_name}'", shell=True)
        return True
    except subprocess.CalledProcessError:
        return False
try:
    # Check if the RD_API_KEY environment variable is set
    if not (os.getenv("RD_API_KEY") is None):
        
        # Check if the RCLONE_MOUNT_NAME environment variable is set
        rclone_mount_name = os.getenv('RCLONE_MOUNT_NAME')
        if rclone_mount_name:
            DIR = f'/data/{rclone_mount_name}/movies'
            if os.path.isdir(DIR):
                exit(0)
            else:
                raise Exception("The rclone mount is not accessible")
    
    # Check if the PLEX_USER environment variable is set
    if not (os.getenv("PLEX_USER") is None):
        process_name = "python"
        arguments = "python /plex_debrid/main.py --config-dir /config"
        if check_plex_debrid():
            sys.exit(0)
        else:
            raise Exception("The plex_debrid process is not running.")
        
except Exception as e:
    # Print the exception
    print(dt(), e)
    exit(1)