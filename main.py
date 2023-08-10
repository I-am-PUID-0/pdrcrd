from base import *
from plex_debrid_ import update, setup 
from rclone_rd import rclone
from cleanup import duplicate_cleanup


def main():
    logger = get_logger()

    version = '1.4.1'

    ascii_art = f'''
                                                                           
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

    logger.info(ascii_art.format(version=version)  + "\n" + "\n")

    def healthcheck():
        while True:
            time.sleep(10)
            try:
                result = subprocess.run(['python', 'healthcheck.py'], capture_output=True, text=True) 
                if result.stderr:
                    logger.error(result.stderr.strip())
            except Exception as e:
                logger.error('Error running healthcheck.py: %s', e)
            time.sleep(50)
    thread = threading.Thread(target=healthcheck)
    thread.daemon = True
    thread.start()

    try:
        if not DUPECLEAN:
            pass
        elif DUPECLEAN:
            duplicate_cleanup.duplicate_cleanup()
    except Exception as e:
        logger.error(e)

    try:
        if RDAPIKEY or ADAPIKEY:
            if RCLONEMN:
                rclone.setup()
        else:
            raise MissingAPIKeyException()
    except Exception as e:
        logger.error(e)

    try:
        if PLEXUSER:
            setup.pd_setup()
            if AUTOUPDATE:
                update.auto_update()
            else:
                update.update_disabled()
    except:
        pass

if __name__ == "__main__":
    main()