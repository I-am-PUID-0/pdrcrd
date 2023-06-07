from json import load, dump
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
import time
import os
import requests
import zipfile
import io
import shutil
import regex
import subprocess
import schedule
import psutil
import sys
import threading


load_dotenv(find_dotenv('./config/.env'))

def get_logger():
    logger_name = "pdrcrd_logger"
    log_directory = './log'
    log_filename = f"pdrcrd_{datetime.now().strftime('%Y-%m-%d')}.log"
    log_path = os.path.join(log_directory, log_filename)

    # Check if a logger with the specified name already exists
    if logger_name in logging.Logger.manager.loggerDict:
        return logging.getLogger(logger_name)

    # Create a new logger and set it up
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%b %e, %Y %H:%M:%S')

    # Create file handler
    file_handler = TimedRotatingFileHandler(log_path, when='midnight', backupCount=7)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Create stream handler
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Redirect stdout to the logger
    sys.stdout = StreamToLogger(logger, logging.INFO)

    return logger

# Custom stream class to redirect stdout to logger
class StreamToLogger:
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass

PLEXUSER = os.getenv('PLEX_USER')
PLEXTOKEN = os.getenv('PLEX_TOKEN')
RDAPIKEY = os.getenv('RD_API_KEY')
PLEXADD = os.getenv('PLEX_ADDRESS')
SHOWMENU = os.getenv('SHOW_MENU')
LOGFILE = os.getenv('PD_LOGFILE')
AUTOUPDATE = os.getenv('AUTO_UPDATE')