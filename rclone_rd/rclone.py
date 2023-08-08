from base import *


def setup():
    logger = get_logger()
    logger.info("Checking rclone_RD flags")

    try:
        if not RCLONEMN:
            raise Exception("Please set a name for the rclone mount")
        logger.info(f"Configuring the rclone mount name to {RCLONEMN}")

        if not RDAPIKEY and not ADAPIKEY:
            raise Exception("Please set the API Key for the rclone mount")
        logger.info("Configuring the API key")

        if RDAPIKEY and ADAPIKEY:
            RCLONEMN_RD = f"{RCLONEMN}_RD"
            RCLONEMN_AD = f"{RCLONEMN}_AD"
        else:
            RCLONEMN_RD = RCLONEMN_AD = RCLONEMN

        with open("/config/rclone.config", "w") as f:
            if RDAPIKEY:
                f.write(f"[{RCLONEMN_RD}]\n")
                f.write("type = realdebrid\n")
                f.write(f"api_key = {RDAPIKEY}\n")
            if ADAPIKEY:
                f.write(f"[{RCLONEMN_AD}]\n")
                f.write("type = webdav\n")
                f.write("url = https://alldebrid.com/webdav/\n")
                f.write("vendor = other\n")
                f.write("pass = lzDDFcDW6megEYv7Oq64qReBamOQ\n")
                f.write(f"user = {ADAPIKEY}\n")

        with open("/etc/fuse.conf", "a") as f:
            f.write("user_allow_other\n")

        mount_names = []
        if RDAPIKEY:
            mount_names.append(RCLONEMN_RD)
        if ADAPIKEY:
            mount_names.append(RCLONEMN_AD)

        for idx, mn in enumerate(mount_names):
            logger.info(f"Configuring rclone_RD for {mn}")
            subprocess.run(["umount", f"/data/{mn}"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            os.makedirs(f"/data/{mn}", exist_ok=True)
            
            if not PLEXUSER:
                if idx != len(mount_names) - 1:  
                    logger.info(f"Starting rclone_RD daemon for {mn}")
                    subprocess.run(["/rclone-linux", "mount", f"{mn}:", f"/data/{mn}", "--config", "/config/rclone.config", "--allow-other", "--poll-interval=0", "--daemon"])
                else:  
                    logger.info(f"Starting rclone_RD for {mn}")
                    subprocess.run(["/rclone-linux", "mount", f"{mn}:", f"/data/{mn}", "--config", "/config/rclone.config", "--allow-other", "--poll-interval=0"])
            else:
                logger.info(f"Starting rclone_RD daemon for {mn}")
                subprocess.run(["/rclone-linux", "mount", f"{mn}:", f"/data/{mn}", "--config", "/config/rclone.config", "--allow-other", "--poll-interval=0", "--daemon"])
                
        logger.info("rclone_RD startup complete")

    except Exception as e:
        logger.error(e)
        exit(1)