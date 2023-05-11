from json import load, dump
#from dotenv import load_dotenv
from datetime import datetime
import time
import os
import requests
import zipfile
import io
import shutil
import regex
import subprocess
import schedule

def dt():
    tnow = datetime.now()
    dt_string = tnow.strftime("%b %e, %Y %H:%M:%S")
    return dt_string

PLEXUSER = os.getenv('PLEX_USER')
PLEXTOKEN = os.getenv('PLEX_TOKEN')
RDAPIKEY = os.getenv('RD_API_KEY')
PLEXADD = os.getenv('PLEX_ADDRESS')
SHOWMENU = os.getenv('SHOW_MENU')
LOGFILE = os.getenv('PD_LOGFILE')
AUTOUPDATE = os.getenv('AUTO_UPDATE')