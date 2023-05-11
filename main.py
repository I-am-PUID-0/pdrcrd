from base import *
from plex_debrid_ import update
from plex_debrid_ import setup
from rclone_rd import rclone


def main():
    try:
        # Check if the RD_API_KEY environment variable is set
        if not (os.getenv("RD_API_KEY") is None):
            # Check if the RCLONE_MOUNT_NAME environment variable is set
            if not (os.getenv("RCLONE_MOUNT_NAME") is None):
                # Call the rclone setup function
                rclone.setup()
        else:
            # Raise an exception if the RD_API_KEY environment variable is not set
            raise Exception(
                "Please set the realdebrid API Key: RD_API_KEY environment variable is missing from the docker-compose file"
            )
    except Exception as e:
        # Print the exception
        print(dt(), e)
    try:
        if not (os.getenv("PLEX_USER") is None):
            # Call the pd_setup function
            setup.pd_setup()
            # Check if the AUTO_UPDATE environment variable is set
            if not (os.getenv("AUTO_UPDATE") is None):
                # Call the auto_update function
                update.auto_update()
            else:
                # Call the update_disabled function
                update.update_disabled()
    except:
        pass
if __name__ == "__main__":
    # Call the main function
    main()