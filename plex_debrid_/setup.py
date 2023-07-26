from base import *


logger = get_logger()

def pd_setup():
    logger.info("Configuring plex_debrid")
    settings_file = "./config/settings.json"

    if not os.path.exists(settings_file):
        subprocess.run(
            ["cp", "./plex_debrid_/settings-default.json", settings_file], check=True
        )

    try:
        if not PLEXUSER:
            raise MissingEnvironmentVariable("PLEX_USER")
        if not PLEXTOKEN:
            raise MissingEnvironmentVariable("PLEX_TOKEN")
        if not RDAPIKEY:
            raise MissingEnvironmentVariable("RD_API_KEY")
        if not PLEXADD:
            raise MissingEnvironmentVariable("PLEX_ADDRESS")

        logger.info("plex_debrid configuration complete")
        logger.info("Starting plex_debrid")

        with open(settings_file, "r+") as f:
            json_data = load(f)
            json_data["Plex users"][0] = [PLEXUSER, PLEXTOKEN]
            json_data["Real Debrid API Key"] = RDAPIKEY
            json_data["Plex server address"] = PLEXADD

            if SHOWMENU is not None:
                json_data["Show Menu on Startup"] = SHOWMENU

            if LOGFILE is not None:
                json_data["Log to file"] = LOGFILE

            f.seek(0)
            dump(json_data, f, indent=4)
            f.truncate()

    except Exception as e:
        logger.error("An error occurred. Exiting...")
        logger.error(str(e))
        raise