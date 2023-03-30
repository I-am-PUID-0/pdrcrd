from json import load, dump
from os import getenv
from dotenv import load_dotenv

load_dotenv()

PLEXUSER = getenv('PLEX_USER')
PLEXTOKEN = getenv('PLEX_TOKEN')
RDAPIKEY = getenv('RD_API_KEY')
PLEXADD = getenv('PLEX_ADDRESS')
SHOWMENU = getenv('SHOW_MENU')
LOGFILE = getenv('PD_LOGFILE')

if not (PLEXUSER is None or PLEXTOKEN is None):
  with open('/config/settings.json', 'r+') as f:
    json_data = load(f)
    json_data['Plex users'][0] = [PLEXUSER, PLEXTOKEN]
    f.seek(0)
    dump(json_data, f, indent=4)
    f.truncate()
else:
  if (PLEXUSER is None and PLEXTOKEN is None):
    print ("PLEX_USER & PLEX_TOKEN environment variables are missing.")
    exit(1)
  elif PLEXTOKEN is None:
    print ("PLEX_TOKEN environment variable is missing.")
    exit(1)
  else:
    print ("PLEX_USER environment variable is missing.")
    exit(1)
    
if not (RDAPIKEY is None):
  with open('/config/settings.json', 'r+') as f:
    json_data = load(f)
    json_data['Real Debrid API Key'] = RDAPIKEY
    f.seek(0)
    dump(json_data, f, indent=4)
    f.truncate()
else:
    print ("RD_API_KEY environment variable is missing.")
    exit(1)

if not (PLEXADD is None):
  with open('/config/settings.json', 'r+') as f:
    json_data = load(f)
    json_data['Plex server address'] = PLEXADD
    f.seek(0)
    dump(json_data, f, indent=4)
    f.truncate()
else:
    print ("PLEX_ADDRESS environment variable is missing.")
    exit(1)
    
if not (SHOWMENU is None):
  with open('/config/settings.json', 'r+') as f:
    json_data = load(f)
    json_data['Show Menu on Startup'] = SHOWMENU
    f.seek(0)
    dump(json_data, f, indent=4)
    f.truncate()
else:
    print ("Using default: Show Menu on Startup=true")    
    
if not (LOGFILE is None):
  with open('/config/settings.json', 'r+') as f:
    json_data = load(f)
    json_data['Log to file'] = LOGFILE
    f.seek(0)
    dump(json_data, f, indent=4)
    f.truncate()
else:
    print ("Using default: Log to file=false")       