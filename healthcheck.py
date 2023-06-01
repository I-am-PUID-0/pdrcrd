from base import *

# Get logger object
logger = get_logger()
# plex_debrid process name
process_name = "python /plex_debrid/main.py --config-dir /config"
# Define check for plex_debrid process
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
        # Check if the rclone mount is accessible
        if rclone_mount_name:
            DIR = f'/data/{rclone_mount_name}/movies'
            if os.path.isdir(DIR):
                exit(0)
            else:
                raise Exception("The rclone mount is not accessible")
    
    # Check if the PLEX_USER environment variable is set
    if not (os.getenv("PLEX_USER") is None):
        # Check if plex_debrid is running
        process_name = "python"
        arguments = "python /plex_debrid/main.py --config-dir /config"
        if check_plex_debrid():
            sys.exit(0)
        else:
            raise Exception("The plex_debrid process is not running.")
        
except Exception as e:
    # Log the exception with the current date and time
    logger.error('%s: %s', dt(), e)
    # Exit with an error code
    exit(1)