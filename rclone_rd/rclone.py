from base import *


def setup():
    # Get logger object
    logger = get_logger()

    # Log the current date and time and check the rclone_RD flags
    logger.info("Checking rclone_RD flags")

    try:
        # Check if the environment variable RCLONE_MOUNT_NAME is set
        if not os.environ.get("RCLONE_MOUNT_NAME"):
            # If not, raise an exception
            raise Exception("Please set a name for the rclone mount")

        # Log the current date and time and configure the rclone mount name
        logger.info(f"Configuring the rclone mount name to {os.environ['RCLONE_MOUNT_NAME']}")

        # Check if the environment variable RD_API_KEY is set
        if not os.environ.get("RD_API_KEY"):
            # If not, raise an exception
            raise Exception("Please set the API Key for the rclone mount")

        # Log the current date and time and configure the API key
        logger.info("Configuring the API key")

        # Log the current date and time and configure rclone_RD
        logger.info("Configuring rclone_RD")
    
        # Unmount the rclone mount
        subprocess.run(["umount", f"/data/{os.environ['RCLONE_MOUNT_NAME']}"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Create the directory for the rclone mount
        os.makedirs(f"/data/{os.environ['RCLONE_MOUNT_NAME']}", exist_ok=True)

        # Create the rclone config file
        with open("/config/rclone.config", "w") as f:
            # Write the mount name to the config file
            f.write(f"[{os.environ['RCLONE_MOUNT_NAME']}]\n")
            # Write the type of mount to the config file
            f.write("type = realdebrid\n")
            # Write the API key to the config file
            f.write(f"api_key = {os.environ['RD_API_KEY']}\n")

        # Append user_allow_other to the fuse config file
        with open("/etc/fuse.conf", "a") as f:
            f.write("user_allow_other\n")
        try:
            if not os.environ.get("PLEX_USER"):
                # Print the current date and time and start rclone_RD
                logger.info("Starting rclone_RD")
                # Mount the rclone mount
                subprocess.run(["/rclone-linux", "mount", f"{os.environ['RCLONE_MOUNT_NAME']}:", f"/data/{os.environ['RCLONE_MOUNT_NAME']}", "--config", "/config/rclone.config", "--allow-other"])
            else:
                # Print the current date and time and start rclone_RD as a daemon
                logger.info("Starting rclone_RD daemon")
                # Mount the rclone mount
                subprocess.run(["/rclone-linux", "mount", f"{os.environ['RCLONE_MOUNT_NAME']}:", f"/data/{os.environ['RCLONE_MOUNT_NAME']}", "--config", "/config/rclone.config", "--allow-other","--daemon"])
        except :
            pass
    # Catch any exceptions
    except Exception as e:
        # Log the exception with the current date and time
        logger.error(e)
        # Exit with an error code
        exit(1)