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
    version = '1.1.2'

    # Create a custom formatter for the ASCII art log message
    class ASCIIArtFormatter(logging.Formatter):
        def format(self, record):
            return record.getMessage()
    # Create a separate handler for the ASCII art log message
    ascii_art_handler = logging.StreamHandler()
    ascii_art_handler.setFormatter(ASCIIArtFormatter())
    logger.addHandler(ascii_art_handler)
    # Log the ASCII art and version number & remove the handler
    logger.info(ascii_art.format(version=version) + "\n" * 2)
    logger.removeHandler(ascii_art_handler)

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
        if not RDAPIKEY:
            # If not, raise an exception
            raise Exception("Please set the realdebrid API Key: RD_API_KEY environment variable is missing from the docker-compose file")

        # Call the rclone setup function
        rclone.setup()
    except Exception as e:
        # Log the exception
        logger.error('%s: %s', dt(), e)

    try:
        if PLEXUSER:
            # Call the pd_setup function
            setup.pd_setup()

            # Check if the AUTO_UPDATE environment variable is set
            if AUTOUPDATE:
                # Call the auto_update function
                update.auto_update()
            else:
                # Call the update_disabled function
                update.update_disabled()
    except Exception as e:
        # Log the exception
        logger.error('%s: %s', dt(), e)

if __name__ == "__main__":
    # Call the main function
    main()