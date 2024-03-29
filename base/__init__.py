from json import load, dump
from dotenv import load_dotenv, find_dotenv
from datetime import datetime, timedelta
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
import glob
import re


load_dotenv(find_dotenv('./config/.env'))

class MissingAPIKeyException(Exception):
    def __init__(self):
        self.message = "Please set the debrid API Key: environment variable is missing from the docker-compose file"
        super().__init__(self.message)

class MissingEnvironmentVariable(Exception):
    def __init__(self, variable_name):
        self.variable_name = variable_name
        message = f"Environment variable '{variable_name}' is missing."
        super().__init__(message)

    def log_exception(self, logger):
        logger.error(f"Missing environment variable: {self.variable_name}")

class ConfigurationError(Exception):
    def __init__(self, error_message):
        self.error_message = error_message
        super().__init__(self.error_message)

def format_time(interval):
    interval_hours = int(interval)
    interval_minutes = int((interval - interval_hours) * 60)

    if interval_hours == 1 and interval_minutes == 0:
        return "1 hour"
    elif interval_hours == 1 and interval_minutes != 0:
        return f"1 hour {interval_minutes} minutes"
    elif interval_hours != 1 and interval_minutes == 0:
        return f"{interval_hours} hours"
    else:
        return f"{interval_hours} hours {interval_minutes} minutes"

def get_start_time():
    start_time = time.time()
    return start_time

def time_to_complete(start_time):
    end_time = time.time()
    elapsed_time = end_time - start_time

    hours = int(elapsed_time // 3600)
    minutes = int((elapsed_time % 3600) // 60)
    seconds = int(elapsed_time % 60)

    time_string = ""
    if hours > 0:
        time_string += f"{hours} hour(s) "
    if minutes > 0:
        time_string += f"{minutes} minute(s) "
    if seconds > 0:
        time_string += f"{seconds} second(s)"
    return time_string

class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False, atTime=None):
        self.rollover_filename = filename
        TimedRotatingFileHandler.__init__(self, self.rollover_filename, when, interval, backupCount, encoding, delay, utc, atTime)

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None

        base_file_name_without_date = self.baseFilename.rsplit('-', 3)[0]
        current_date = time.strftime("%Y-%m-%d")
        correct_filename = base_file_name_without_date + '-' + current_date + '.log'

        if self.rollover_filename != correct_filename:
            new_filename = correct_filename
        else:
            new_filename = self.rollover_filename

        filenames_to_delete = self.getFilesToDelete()
        for filename in filenames_to_delete:
            os.remove(filename)

        self.rollover_filename = new_filename
        self.baseFilename = self.rollover_filename
        self.stream = self._open()

        new_rollover_at = self.computeRollover(self.rolloverAt)
        while new_rollover_at <= time.time():
            new_rollover_at = new_rollover_at + self.interval
        if self.utc:
            dst_at_rollover = time.localtime(new_rollover_at)[-1]
        else:
            dst_at_rollover = time.gmtime(new_rollover_at)[-1]

        if time.localtime(time.time())[-1] != dst_at_rollover:
            addend = -3600 if time.localtime(time.time())[-1] else 3600
            new_rollover_at += addend
        self.rolloverAt = new_rollover_at

    def getFilesToDelete(self):
        dirName, baseName = os.path.split(self.baseFilename)
        fileNames = os.listdir(dirName)
        result = []
        prefix = baseName.split('-', 1)[0] + "-"
        plen = len(prefix)
        for fileName in fileNames:
            if fileName[:plen] == prefix:
                suffix = fileName[plen:]
                if re.compile(r"^\d{4}-\d{2}-\d{2}.log$").match(suffix):
                    result.append(os.path.join(dirName, fileName))
        result.sort()
        if len(result) < self.backupCount:
            result = []
        else:
            result = result[:len(result) - self.backupCount]
        return result

def get_logger(log_name='pdrcrd', log_dir='./log'):
    current_date = time.strftime("%Y-%m-%d")
    log_filename = f"{log_name}-{current_date}.log"
    logger = logging.getLogger(log_name)
    backupCount_env = os.getenv('PDRCRD_LOG_COUNT')
    try:
        backupCount = int(backupCount_env)
    except (ValueError, TypeError):
        backupCount = 2
    log_level_env = os.getenv('PDRCRD_LOG_LEVEL')
    if log_level_env:
        log_level = log_level_env.upper()
    else:
        log_level = 'INFO'
    numeric_level = getattr(logging, log_level, logging.INFO)
    logger.setLevel(numeric_level)
    log_path = os.path.join(log_dir, log_filename)
    handler = CustomTimedRotatingFileHandler(log_path, when="midnight", interval=1, backupCount=backupCount)
    os.chmod(log_path, 0o666)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%b %e, %Y %H:%M:%S')
    handler.setFormatter(formatter)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)

    for hdlr in logger.handlers[:]:
        logger.removeHandler(hdlr)
    logger.addHandler(handler)
    logger.addHandler(stdout_handler)
    return logger


PLEXUSER = os.getenv('PLEX_USER')
PLEXTOKEN = os.getenv('PLEX_TOKEN')
RDAPIKEY = os.getenv('RD_API_KEY')
ADAPIKEY = os.getenv('AD_API_KEY')
PLEXADD = os.getenv('PLEX_ADDRESS')
SHOWMENU = os.getenv('SHOW_MENU')
LOGFILE = os.getenv('PD_LOGFILE')
AUTOUPDATE = os.getenv('AUTO_UPDATE')
DUPECLEAN = os.getenv('DUPLICATE_CLEANUP')
CLEANUPINT = os.getenv('CLEANUP_INTERVAL')
RCLONEMN = os.getenv("RCLONE_MOUNT_NAME")