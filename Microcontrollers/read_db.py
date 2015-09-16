#!/usr/bin/env python
'''Script to pull information from RDS database'''

def retrieve_actions():
    '''Attempts to connection to RDS instance and retrieve data'''
    # Import psycopg2 dbc
    import psycopg2
    # Import os to access environmental variables
    import os

    # Attempt to create connection to RDS database
    try:
        conn = psycopg2.connect(dbname='microcontrollers',
                                user=os.environ['AWS_USER'],
                                host=os.environ['AWS_HOST'],
                                password=os.environ['AWS_PWD'],
                                port=os.environ['AWS_PORT'],)
    except:
        print "Couldn't establish RDS connection"

    # Attempt to get cursor
    try:
        c = conn.cursor()
    except:
        print "Couldn't get cursor"

    # Attempt to execute query
    try:
        c.execute('SELECT * FROM "Receiver_action";')
    except:
        print "Couldn't query RDS"

    # Attempt to get column names from cursor
    try:
        columns = [column[0] for column in c.description]
    except:
        print "Couldn't retrieve columns"

    # Create dictionary of column names and values for each result
    try:
        results = []
        for row in c.fetchall():
            results.append(dict(zip(columns, row)))
    except:
        print "Couldn't print results"

    conn.close()
    return results
