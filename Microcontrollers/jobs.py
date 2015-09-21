#!/usr/bin/env python
'''Script to schedule cron job for user-provided actions https://pypi.python.org/pypi/python-crontab'''
from crontab import CronTab, CronItem
import os
import sys
import django
from datetime import datetime as dt
from read_db import retrieve_actions as rt

def retrieve_jobs():
    ''' Return list of user's cron jobs'''
    cron = CronTab(user=True)
    jobs = []
    for job in cron:
        out = 'Job #%s \n' % str(job.comment)
        out += 'Command %s' % str(job.command)
        jobs.append(out)
    return jobs

def schedule_job():
    ''' Attempt to schedule new cron job for user '''
    # Try to retrieve actions
    try:
        jobs = rt()
        
        # Try to create crontab
        try:
            cron = CronTab(user=True)

            try:
                # Iterate over list of dictionaries
                for job in jobs:
                    # Get values for job
                    job_id = job['id']
                    node_id = job['node_id']
                    sensor_id = job['sensor_id']
                    dt = job['datetime_to_execute']
                    recurrence = job['recurrence_textbox']

                    # Try to create a new job
                    try:
                        cron.remove_all(comment=str(job_id))
                        new_job = cron.new(command='python /home/pi/ccasp/Microcontrollers/jobs.py execute %s %s %s' %
                                           (node_id, sensor_id, job_id),
                                           comment=str(job_id))
                        
                        # Try to set time for job
                        try:
                            if recurrence == 'None':
                                new_job.setall(dt.minute, dt.hour,
                                               dt.day, dt.month, None)
                            else:
                                if recurrence == 'Daily':
                                    new_job.setall(dt.minute, dt.hour,
                                                   None, None, None)
                                elif recurrence == 'Weekly':
                                    new_job.setall(dt.minute, dt.hour,
                                                   None, None, dt.weekday)
                                elif recurrence == 'Monthly':
                                    new_job.setall(dt.minute, dt.hour,
                                                   dt.day, None, None)
                            # Try to write job
                            try:
                                cron.write()
                            except:
                                print "Error writing cron job"
                        except:
                            print "Error setting job time"
                    except:
                        print "Error creating new job"
            except:
                print "Error retrieving values"
        except:
            print "Error creating crontab"
    except:
        print "Error retrieving actions"

def execute_job(node_id, sensor_id, job_id):
    '''
    Attempt to execute job for given node and sensor
    @param node_id: the node
    @param sensor_id: the sensor
    '''
    # Set environment for creating Django models
    import django
    from django.conf import settings
    from django.core.management import call_command
    sys.path.insert(1, '/home/pi/ccasp/Microcontrollers/Microcontrollers')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    django.setup()
    
    # Set up logging
    import logging
    logging.basicConfig(filename=
                        '/home/pi/ccasp/Microcontrollers/jobs.txt', level=logging.INFO)
    
    logging.info('Starting execute job')
    if len(sys.argv) != 5:
        print 'usage -- jobs.py execute node sensor job'
        logging.info('Invalid sys.argv')
        sys.exit(1)
    
    try:
        logging.info('Received job for node %s sensor %s job %s' % (node_id, sensor_id, job_id))
        cron = CronTab(user=True)
        call_command('add_action', (job_id,))
        logging.info('Saved job %s to database' % job_id)            
    except:
        logging.info('Could not save job %s to database' % job_id)
        
    # TODO Send message to Arduino Master over serial
    # Wait for return value 

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'schedule':
            schedule_job()
        elif sys.argv[1] == 'execute':
            if len(sys.argv) == 5:
                execute_job(sys.argv[2], sys.argv[3], sys.argv[4])
            else:
                print 'usage -- jobs.py execute node_id sensor_id job_id'
                sys.exit(1)
        elif sys.argv[1] == 'retrieve':
            for job in retrieve_jobs():
                print job
        else:
            print 'usage -- jobs.py schedule|execute node sensor'
            sys.exit(1)
    else:
        print 'usage -- jobs.py schedule|execute node sensor'
        sys.exit(1)
