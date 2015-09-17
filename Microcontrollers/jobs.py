#!/usr/bin/env python
'''Script to schedule cron job for user-provided actions'''
from crontab import CronTab
import sys
from datetime import datetime as dt
from read_db import retrieve_actions as rt

def schedule_job():
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

                    # Try to create a new job
                    try:
                        #new_job = cron.new(command='python jobs.py execute %s %s', node_id, sensor_id)
                        new_job = cron.new(command='echo "Test"', comment=str(job_id))
                        # Try to set time for job
                        try:
                            new_job.setall(dt.minute, dt.hour,
                                           dt.day, dt.month, None)
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

def execute_job():
    if len(sys.argv) != 4:
        print 'usage -- jobs.py execute node sensor'
        sys.exit(1)
    
    node_id = sys.argv[2]
    sensor_id = sys.argv[3]
    
    # Send message to Arduino Master over serial
    # Wait for return value 

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'schedule':
            schedule_job()
        elif sys.argv[1] == 'execute':
            execute_job()
        else:
            print 'usage -- jobs.py schedule|execute node sensor'
            sys.exit(1)
    else:
        print 'usage -- jobs.py schedule|execute node sensor'
        sys.exit(1)
