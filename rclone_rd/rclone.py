from base import *


def setup():
    logger = get_logger()
    logger.info("Checking rclone_RD flags")

    try:
        if not os.environ.get("RCLONE_MOUNT_NAME"):
            raise Exception("Please set a name for the rclone mount")
        logger.info(f"Configuring the rclone mount name to {os.environ['RCLONE_MOUNT_NAME']}")

        if not os.environ.get("RD_API_KEY"):
            raise Exception("Please set the API Key for the rclone mount")
        logger.info("Configuring the API key")

        logger.info("Configuring rclone_RD")
        subprocess.run(["umount", f"/data/{os.environ['RCLONE_MOUNT_NAME']}"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.makedirs(f"/data/{os.environ['RCLONE_MOUNT_NAME']}", exist_ok=True)
        with open("/config/rclone.config", "w") as f:
            f.write(f"[{os.environ['RCLONE_MOUNT_NAME']}]\n")
            f.write("type = realdebrid\n")
            f.write(f"api_key = {os.environ['RD_API_KEY']}\n")
        with open("/etc/fuse.conf", "a") as f:
            f.write("user_allow_other\n")
        try:
            if not os.environ.get("PLEX_USER"):
                logger.info("Starting rclone_RD")
                subprocess.run(["/rclone-linux", "mount", f"{os.environ['RCLONE_MOUNT_NAME']}:", f"/data/{os.environ['RCLONE_MOUNT_NAME']}", "--config", "/config/rclone.config", "--allow-other"])
            else:
                logger.info("Starting rclone_RD daemon")
                subprocess.run(["/rclone-linux", "mount", f"{os.environ['RCLONE_MOUNT_NAME']}:", f"/data/{os.environ['RCLONE_MOUNT_NAME']}", "--config", "/config/rclone.config", "--allow-other","--daemon"])
                logger.info("rclone_RD startup complete")                
        except :
            pass
    except Exception as e:
        logger.error(e)
        exit(1)