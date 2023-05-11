from base import *

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
        arguments = "/plex_debrid/main.py --config-dir /config"
        for process in psutil.process_iter():
            try:
                cmdline = process.cmdline()
                if process_name in cmdline and arguments in cmdline:
                    sys.exit(0)
            except (psutil.AccessDenied, psutil.ZombieProcess):
                pass
        raise Exception("The plex_debrid process is not running.")
    
    # Otherwise, raise an exception
    raise Exception("An error occurred while performing the healthcheck")
        
except Exception as e:
    # Print the exception
    print(dt(), e)
    exit(1)