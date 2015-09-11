#!/usr/bin/env python
'''Sends commands to Arduino master controller, receives responses, and
calls Django management command to commit new record to database'''

import serial
import time
from django.conf import settings
from django.core.management import call_command
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

# Open serial connection and wait
# TTY PORT defined in Microcontroller/Microcontroller/settings
# Haven't written logic to grep for /tty/ACM* yet, so adjust manually if needed
ser = serial.Serial(settings.TTY_PORT, 9600)
time.sleep(2)

while True:
    try:
        ser.write('6')
    except:
        print "Failed to write dump data command"

    time.sleep(3)
    while ser.inWaiting() > 0:

        # Read in node UUID
        try:
            node = ser.readline()
            time.sleep(1)
        except:
            print "Failed to read node UUID"
            continue
        try:
            # Read in sensor values
            val = ser.readline()
            # Parse and create Fahrenheit value
            val = val.replace('\n', '')
            val = val.replace('\r', '')
            val = (float(val) * (9.0/5.0)) + 32.0
            val = val - float(node) * 10
            val = str(val)
        except:
            print "Failed to read values"
            continue
    
        # Add record to database
        # call_comment executes a Django management command found in
        #Receiver/management/commands
        call_command('add_record', (node, val,))
        # Update frequency
        time.sleep(120)

# Close serial connection
ser.close()
