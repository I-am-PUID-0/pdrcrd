from base import *


def pd_setup():
    print(dt(), "Configuring plex_debrid")
    settings_file = "/config/settings.json"
    # Check if settings file exists, if not, copy default settings
    if not os.path.exists(settings_file):
        subprocess.run(
            ["cp", "/plex_debrid_/settings-default.json", settings_file], check=True
        )
    try:
        # Check if PLEXUSER and PLEXTOKEN environment variables are set
        if not (PLEXUSER is None or PLEXTOKEN is None):
            # If set, open settings file and update with PLEXUSER and PLEXTOKEN
            with open("/config/settings.json", "r+") as f:
                json_data = load(f)
                json_data["Plex users"][0] = [PLEXUSER, PLEXTOKEN]
                f.seek(0)
                dump(json_data, f, indent=4)
                f.truncate()
        else:
            # If not set, check which environment variable is missing and exit
            if PLEXUSER is None and PLEXTOKEN is None:
                print(dt(), "PLEX_USER & PLEX_TOKEN environment variables are missing.")
                exit(1)
            elif PLEXTOKEN is None:
                print(dt(), "PLEX_TOKEN environment variable is missing.")
                exit(1)
            else:
                print(dt(), "PLEX_USER environment variable is missing.")
                exit(1)

        # Check if RDAPIKEY environment variable is set
        if not (RDAPIKEY is None):
            # If set, open settings file and update with RDAPIKEY
            with open("/config/settings.json", "r+") as f:
                json_data = load(f)
                json_data["Real Debrid API Key"] = RDAPIKEY
                f.seek(0)
                dump(json_data, f, indent=4)
                f.truncate()
        else:
            print(dt(), "RD_API_KEY environment variable is missing.")
            exit(1)

        # Check if PLEXADD environment variable is set
        if not (PLEXADD is None):
            # If set, open settings file and update with PLEXADD
            with open("/config/settings.json", "r+") as f:
                json_data = load(f)
                json_data["Plex server address"] = PLEXADD
                f.seek(0)
                dump(json_data, f, indent=4)
                f.truncate()
        else:
            print(dt(), "PLEX_ADDRESS environment variable is missing.")
            exit(1)

        # Check if SHOWMENU environment variable is set
        if not (SHOWMENU is None):
            # If set, open settings file and update with SHOWMENU
            with open("/config/settings.json", "r+") as f:
                json_data = load(f)
                json_data["Show Menu on Startup"] = SHOWMENU
                f.seek(0)
                dump(json_data, f, indent=4)
                f.truncate()
        else:
            print(dt(), "Using default: Show Menu on Startup=true")

        # Check if LOGFILE environment variable is set
        if not (LOGFILE is None):
            # If set, open settings file and update with LOGFILE
            with open("/config/settings.json", "r+") as f:
                json_data = load(f)
                json_data["Log to file"] = LOGFILE
                f.seek(0)
                dump(json_data, f, indent=4)
                f.truncate()
        else:
            print(dt(), "Using default: Log to file=false")

        print(dt(), "plex_debrid configuration complete")
        print(
            dt(),
            "To ensure that Plex can access the rclone_RD mount, and that plex_debrid can access Plex, please restart Plex now",
        )
        print(dt(), "The script will wait till the restart is complete")

        # Wait for 30 seconds
        for i in range(30):
            print(".", end="", flush=True)
            time.sleep(1)

        print("\n"f"{dt()}"" Waiting for Plex to restart...")
        sp = "/-\|"
        # Check if Plex is running
        while (
            subprocess.run(
                ["wget", "--wait=1", "--tries=0", "--spider", PLEXADD + "/identity"],
                capture_output=True,
            ).returncode
            != 0
        ):
            sp = sp[1:] + sp[0]
            print(f"\r{sp}", end="", flush=True)
            time.sleep(1)

        print("\n"f"{dt()}"" Waiting 30s for Plex to finish starting")
        # Wait for 30 seconds
        for i in range(30):
            print(".", end="", flush=True)
            time.sleep(1)

        print("\n"f"{dt()}"" Starting plex_debrid")
    except:
        print(dt(), "An error occurred. Exiting...")
        exit(1)