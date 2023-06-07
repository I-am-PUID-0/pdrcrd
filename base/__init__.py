from json import load, dump
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
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
    log_filename = "pdrcrd.log"
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
    file_handler = RotatingFileHandler(log_path, maxBytes=1024*1024, backupCount=7)
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

# Check if the log file needs to be rotated based on date change
def check_log_rotation(log_handler):
    current_date = datetime.now().date()
    log_filename = log_handler.baseFilename
    log_file_date = datetime.strptime(log_filename, 'pdrcrd_%Y-%m-%d.log').date()
    
    if current_date > log_file_date:
        log_handler.doRollover()
        new_log_filename = f"pdrcrd_{current_date.strftime('%Y-%m-%d')}.log"
        log_handler.baseFilename = os.path.join(log_handler.baseFilename.rsplit('/', 1)[0], new_log_filename)

# Set up the log rotation check schedule
def schedule_log_rotation_check():
    logger = logging.getLogger("pdrcrd_logger")
    log_handler = logger.handlers[0] 

    # Schedule log rotation check to run at midnight
    midnight = (datetime.now() + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    seconds_until_midnight = (midnight - datetime.now()).total_seconds()
    threading.Timer(seconds_until_midnight, check_log_rotation, args=[log_handler]).start()


def manage_log_files(log_directory, max_backups):
    log_files = []

    # Get all files in the log directory
    for filename in os.listdir(log_directory):
        file_path = os.path.join(log_directory, filename)

        # Only consider log files with the expected format
        if filename.startswith("pdrcrd_") and filename.endswith(".log"):
            log_files.append(file_path)

    # Sort log files based on modification time (oldest to newest)
    log_files.sort(key=os.path.getmtime)

    # Check if the number of log files exceeds the maximum allowed backups
    if len(log_files) > max_backups:
        # Calculate the number of files to delete
        num_files_to_delete = len(log_files) - max_backups

        # Delete the oldest log files
        for i in range(num_files_to_delete):
            os.remove(log_files[i])

# log file management
log_directory = './log'
max_backups = 7
manage_log_files(log_directory, max_backups)
schedule_log_rotation_check()

PLEXUSER = os.getenv('PLEX_USER')
PLEXTOKEN = os.getenv('PLEX_TOKEN')
RDAPIKEY = os.getenv('RD_API_KEY')
PLEXADD = os.getenv('PLEX_ADDRESS')
SHOWMENU = os.getenv('SHOW_MENU')
LOGFILE = os.getenv('PD_LOGFILE')
AUTOUPDATE = os.getenv('AUTO_UPDATE')