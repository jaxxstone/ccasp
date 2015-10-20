#!/usr/bin/env python
'''Sends commands to Arduino master controller, receives responses, and
calls Django management command to commit new record to database'''

import serial
import time
import os
import sys
import django
import logging
import logging.handlers

# Set up logging
LOG_FILENAME = '/tmp/read_data.log'
LOG_LEVEL = logging.INFO

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class MyLogger(object):
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level

    def write(self, message):
        if message.rstrip() != '':
            self.logger.log(self.level, message.rstrip())

sys.stdout = MyLogger(logger, logging.INFO)
sys.stderr = MyLogger(logger, logging.ERROR)

logger.info('Starting')

# Set environment for creating Django models
sys.path.insert(1, '/home/pi/ccasp/Microcontrollers/Microcontrollers')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()
from django.conf import settings
from django.core.management import call_command

# Open serial connection and wait
# TTY PORT defined in Microcontroller/Microcontroller/settings
try:
    ser = serial.Serial(settings.TTY_PORT, 9600)
    time.sleep(2)
except:
    logger.info('Unable to open serial connection')
    sys.exit(1)

while True:
    try:
        ser.write('6')
    except:
        logger.info('Unable to write to serial port')
        sys.exit(1)

    time.sleep(5)
    while ser.inWaiting() > 0:

        # Read in sensor UUID
        try:
            sensor = ser.readline()
            sensor = sensor.rstrip('\r\n')
            time.sleep(1)
        except:
            logger.info('Unable to read from serial')
            continue
        
        # Read in sensor values
        try:
            val = ser.readline()
            val = val.rstrip('\r\n')
        except:
            logger.info('Unable to read values')
            continue
    
        # Add record to database
        # call_comment executes a Django management command found in
        # Receiver/management/commands
        try:
            call_command('add_record', (sensor, val,))
        except:
            logger.info('Unable to add record')

    # Update frequency
    time.sleep(10)

# Close serial connection
ser.close()
