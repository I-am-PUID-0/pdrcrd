from base import *
from plex_debrid_ import update
from plex_debrid_ import setup
from rclone_rd import rclone


def main():
    # Get logger object
    logger = get_logger()

    # ASCII art and version number
    ascii_art = '''
                                                                           
                      88                                               88  
                      88                                               88  
                      88                                               88  
8b,dPPYba,    ,adPPYb,88  8b,dPPYba,   ,adPPYba,  8b,dPPYba,   ,adPPYb,88  
88P'    "8a  a8"    `Y88  88P'   "Y8  a8"     ""  88P'   "Y8  a8"    `Y88  
88       d8  8b       88  88          8b          88          8b       88  
88b,   ,a8"  "8a,   ,d88  88          "8a,   ,aa  88          "8a,   ,d88  
88`YbbdP"'    `"8bbdP"Y8  88           `"Ybbd8"'  88           `"8bbdP"Y8  
88                                                                         
88                        Version: {version}                                    
'''

    # Version number
    version = '1.2.3'

    # Log the ASCII art and version number
    logger.info(ascii_art.format(version=version)  + "\n" + "\n")

    # Define healthcheck
    def healthcheck():
        while True:
            try:
                # Run healthcheck.py and capture the output
                result = subprocess.run(['python', 'healthcheck.py'], capture_output=True, text=True) 
                # Log any error messages
                if result.stderr:
                    logger.error(result.stderr)
            except Exception as e:
                logger.error('Error running healthcheck.py: %s', e)
            time.sleep(60)
    thread = threading.Thread(target=healthcheck)
    thread.daemon = True
    thread.start()

    try:
        # Check if the RD_API_KEY environment variable is set
        if not RDAPIKEY is None:
            if not (os.getenv("RCLONE_MOUNT_NAME") is None):
                # Call the rclone setup function
                rclone.setup()
        else:
            # Raise an exception if the RD_API_KEY environment variable is not set
            raise Exception(
                "Please set the realdebrid API Key: RD_API_KEY environment variable is missing from the docker-compose file"
            )
    except Exception as e:
        # Log the exception
        logger.error(e)

    try:
        if not PLEXUSER is None:
            # Call the pd_setup function
            setup.pd_setup()

            # Check if the AUTO_UPDATE environment variable is set
            if not AUTOUPDATE is None:
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