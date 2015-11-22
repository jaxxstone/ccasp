#!/usr/bin/env python
'''Sends commands to Arduino master controller, receives responses, and
calls Django management command to commit new record to database'''

import serial
import time
import os
import subprocess
import sys
import django
import logging
import logging.handlers
import mandrill

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
from Receiver.models import UserProfile
import datetime

# Setup Mandrill client for e-mail notifications
mandrill_client = mandrill.Mandrill('')
last_issue = datetime.datetime.now()

# Setup send-to
send_to = UserProfile.objects.filter(
    notifications=True).values('user__email', 'user__first_name', 'user__last_name')

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
    success = True
    while ser.inWaiting() > 0:

        # Read in sensor UUID
        try:
            sensor = ser.readline()
            sensor = sensor.rstrip('\r\n')
            time.sleep(1)
        except:
            logger.info('Unable to read from serial')
            success = False
            continue
        
        # Read in sensor values
        try:
            val = ser.readline()
            val = val.rstrip('\r\n')
        except:
            logger.info('Unable to read values')
            success = False
            continue
    
        # Add record to database
        # call_comment executes a Django management command found in
        # Receiver/management/commands
        try:
            call_command('add_record', (sensor, val,))
        except:
            success = False
            logger.info('Unable to add record')

    # Restart if error
    if success is False:
        if datetime.timedelta(datetime.datetime.now(), last_issue).min > 60:
            try:
                for user in send_to:
                    message = {'from_email': 'robert.lacher@gmail.com',
                               'from_name': 'Robert Lacher',
                               'html': '<p>The Raspberry Pi has stopped updating.</p>',
                               'to': {'email': user.user__email,
                                      'name' : '%s %s' % (user.user__first_name,
                                                          user.user__last_name),
                                      'type': 'to'
                                      }
                               }
                    result = mandrill_client.messages.send(message=message, async=False,
                                                           ip_pool='Main Pool')
            except mandril.Error, e:
                logger.info('A mandrill error occurred: %s - %s' % (e.__class__, e))
        else:
            pass

        try:
            logger.info('Trying to restart daemon...')
            if subprocess.call(
                    ['sudo', 'service', 'read_data.sh', 'restart']) == 0:
                logger.info('Restarted daemon')
            else:
                logging.info('Not sure if exception is raised')
        except:
            logger.info('Failed to restart daemon')
    else:
        pass
            
    # Update frequency
    time.sleep(60)
                       

# Close serial connection
ser.close()
