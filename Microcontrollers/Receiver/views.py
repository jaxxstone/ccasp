'''This module contains the presentation logic for the Receiver application
in the Microcontrollers project. It creates and renders the user-generated
reports, status pages, etc.'''

from django.shortcuts import render
from Receiver.models import Node, Record, Sensor
from Receiver.forms import CustomReport
import json
import os
from django.utils import timezone
from datetime import datetime as dt, timedelta
from django.contrib.auth.decorators import login_required
from dateutil import parser
from Microcontrollers import settings

@login_required(login_url='login.html')
def daily_report(request, nodeid=None, sensorid=None):
    '''
    Return all records from today.
    @param request: the HTTP GET request
    @param nodeid: the Node UUID to generate the report with. Default is None.
    @return: rendered report.html containing a list comprised of Node objects
    and that Node's Sensor values recorded over the past 24 hours
    '''
    time_format = "%Y-%m-%d %H:%M:%S"
    nodes = Node.objects.get(pk=nodeid)
    sensor = Sensor.objects.get(node=nodes, pk=sensorid)
    sensor_type = sensor.type
    sensor_unit = sensor.unit
    my_node_list = []
    sensor_records = sensor.get_records_for_today()
    values = []
    for record in sensor_records:
        # Get time that record was added
        my_time = record.time_recorded
        # Format time as string
        my_time = my_time.strftime(time_format)
        # Convert to Epoch time (in ms) for Highcharts
        my_time = int(dt.strptime(my_time, time_format).strftime('%s'))
        my_time *= 1000
        # Append to list
        # Highcharts requires [time, value] format for datetime graph
        values.append([my_time, record.value])
        # Add node and sensor values list to main list
    my_node_list.append([sensor.id, values])

    return render(request, 'report.html',
                  {'request': request,
                   'node_list': my_node_list,
                   'type': 'Daily',
                   'sensor_type': sensor_type,
                   'sensor_unit': sensor_unit,
                   'sensor_name': sensor.name,})

@login_required(login_url='login.html')
def weekly_report(request, nodeid=None, sensorid=None):
    '''
    Return all records from the past week.
    @param request: the HTTP GET request
    @param nodeid: the Node UUID to generate the report with. Default is None.
    @return: rendered report.html containing a list comprised of Node objects
    and that Node's Sensor values recorded over the past 7 days
    '''
    time_format = "%Y-%m-%d %H:%M:%S"
    nodes = Node.objects.get(pk=nodeid)
    sensor = Sensor.objects.get(node=nodes, pk=sensorid)
    sensor_type = sensor.type
    sensor_unit = sensor.unit
    my_node_list = []
    sensor_records = sensor.get_records_for_week()
    values = []
    for record in sensor_records:
        # Get time that record was added
        my_time = record.time_recorded
        # Format time as string
        my_time = my_time.strftime(time_format)
        # Convert to Epoch time (in ms) for Highcharts
        my_time = int(dt.strptime(my_time, time_format).strftime('%s'))
        my_time *= 1000
        # Append to list
        # Highcharts requires [time, value] format for datetime graph
        values.append([my_time, record.value])
        # Add node and sensor values list to main list
    my_node_list.append([sensor.id, values])

    return render(request, 'report.html',
                  {'request': request,
                   'node_list': my_node_list,
                   'type': 'Weekly',
                   'sensor_type': sensor_type,
                   'sensor_unit': sensor_unit,
                   'sensor_name': sensor.name,})

@login_required(login_url='login.html')
def monthly_report(request, nodeid=None, sensorid=None):
    '''
    Return all records from the past month.
    @param request: the HTTP GET request
    @param nodeid: the Node UUID to generate the report with. Default is None.
    @return: rendered report.html containing a list comprised of Node objects
    and that Node's Sensor values recorded over the past 31 days
    '''
    time_format = "%Y-%m-%d %H:%M:%S"
    nodes = Node.objects.get(pk=nodeid)
    sensor = Sensor.objects.get(node=nodes, pk=sensorid)
    sensor_type = sensor.type
    sensor_unit = sensor.unit
    my_node_list = []
    sensor_records = sensor.get_records_for_month()
    values = []
    for record in sensor_records:
        # Get time that record was added
        my_time = record.time_recorded
        # Format time as string
        my_time = my_time.strftime(time_format)
        # Convert to Epoch time (in ms) for Highcharts
        my_time = int(dt.strptime(my_time, time_format).strftime('%s'))
        my_time *= 1000
        # Append to list
        # Highcharts requires [time, value] format for datetime graph
        values.append([my_time, record.value])
        # Add node and sensor values list to main list
    my_node_list.append([sensor.id, values])

    return render(request, 'report.html',
                  {'request': request,
                   'node_list': my_node_list,
                   'type': 'Monthly',
                   'sensor_type': sensor_type,
                   'sensor_unit': sensor_unit,
                   'sensor_name': sensor.name,})

@login_required(login_url='login.html')
def yearly_report(request, nodeid=None, sensorid=None):
    '''
    Return all records from the past year.
    @param request: the HTTP GET request
    @param nodeid: the Node UUID to generate the report with. Default is None.
    @return: rendered report.html containing a list comprised of Node objects
    and that Node's Sensor values recorded over the past 365 days
    '''
    time_format = "%Y-%m-%d %H:%M:%S"
    nodes = Node.objects.get(pk=nodeid)
    sensor = Sensor.objects.get(node=nodes, pk=sensorid)
    sensor_type = sensor.type
    sensor_unit = sensor.unit
    my_node_list = []
    sensor_records = sensor.get_records_for_year()
    values = []
    for record in sensor_records:
        # Get time that record was added
        my_time = record.time_recorded
        # Format time as string
        my_time = my_time.strftime(time_format)
        # Convert to Epoch time (in ms) for Highcharts
        my_time = int(dt.strptime(my_time, time_format).strftime('%s'))
        my_time *= 1000
        # Append to list
        # Highcharts requires [time, value] format for datetime graph
        values.append([my_time, record.value])
        # Add node and sensor values list to main list
    my_node_list.append([sensor.id, values])

    return render(request, 'report.html',
                  {'request': request,
                   'node_list': my_node_list,
                   'type': 'Yearly',
                   'sensor_type': sensor_type,
                   'sensor_unit': sensor_unit,
                   'sensor_name': sensor.name,})

@login_required(login_url='login.html')
def custom_form(request, nodeid=None, sensorid=None, invalid=None):
    '''
    Returns a form used to generate a custom report
    @param request: the HTTP GET request
    @param invalid: Boolean value indicating whether the start and
    end datetime ranges are valid
    @param nodeid: the Node UUID to generate the report with. Default is None.
    @return: rendered custom.html containing a CustomReport form model.
    Returns an invalid flag if there were errors.
    '''
    if request.method == 'GET':
        form = CustomReport()

    if invalid:
        return render(request, 'custom.html',
                      {'form': form,
                       'error': True,})
    else:
        return render(request, 'custom.html',
                      {'form': form,
                       'nodeid': nodeid,
                       'sensorid': sensorid,})

@login_required(login_url='login.html')
def custom_report(request, nodeid=None, sensorid=None):
    '''
    Returns the custom report requested by the user
    @param request: the HTTP GET request
    @return: rendered report.html containing a list comprised of Node objects
    and that Node's Sensor values recorded over the requested time period
    '''
    # Retrieve dates and times from request
    start_date = request.GET['startDate']
    start_time = request.GET['startTime']
    end_date = request.GET['endDate']
    end_time = request.GET['endTime']
    offset = request.GET['tzOffset']

    # Convert offset minutes to ms
    offset = int(offset) * 60 * 1000

    # string format for time
    time_format = '%Y-%m-%d %H:%M'
    start_string = start_date + ' ' + start_time
    end_string = end_date + ' ' + end_time

    # Create new datetime from strings
    start = timezone.datetime.strptime(start_string, time_format)
    end = timezone.datetime.strptime(end_string, time_format)

    # Make datetime aware of timezone
    start = timezone.make_aware(start)
    end = timezone.make_aware(end)

    # Add offset to current time
    # Need to do this because time received from request is considered UTC
    # Highcharts will change it to localtime resulting in discrepancy
    start = start + timezone.timedelta(0, 0, 0, offset)
    end = end + timezone.timedelta(0, 0, 0, offset)

    # Make sure start and end ranges are valid
    if end < start:
        return custom_form(request, invalid=True)

    # Retrieve records
    my_node_list = []
    node = Node.objects.get(node_id=nodeid)
    sensor = Sensor.objects.get(node=node, pk=sensorid)
    sensor_type = sensor.type
    unit = sensor.unit
    records = sensor.get_records_for_custom(start, end)

    values = []
    for record in records:
        # Get time that record was added
        my_time = record.time_recorded
        # Format time as string
        my_time = my_time.strftime(time_format)
        # Convert to Epoch time for Highcharts
        my_time = int(dt.strptime(my_time, time_format).strftime('%s'))
        my_time *= 1000
        # Append to list
        # Highcharts requires [time, value] format for datetime graph
        values.append([my_time, record.value])

    # Add node and sensor values list to main list
    my_node_list.append([sensor.id, values])

    # Convert start and end to Epoch time for chart ranges
    start = start.strftime(time_format)
    start = int(dt.strptime(start, time_format).strftime('%s')) * 1000
    end = end.strftime(time_format)
    end = int(dt.strptime(end, time_format).strftime('%s')) * 1000

    return render(request, 'report.html',
                  {'request': request,
                   'node_list': my_node_list,
                   'sensor_type': 'Custom Range',
                   'min': json.dumps(start),
                   'max': end,
                   'sensor_type': sensor_type,
                   'sensor_unit': unit,
                   'sensor_name': sensor.name,})

@login_required(login_url='login.html')
def overview(request):
    '''
    Return the 100 most recent Records recorded for all Nodes and Sensors
    @param request: the HTTP GET request
    @return: rendered overview.html containing the Node objects and Records
    '''
    # records will hold list of records for each node
    records = Record.objects.values('node__name', 'sensor__name', 'value', 'time_recorded').order_by('time_recorded').reverse()[:100]
    # Return rendered template
    return render(request, 'overview.html',
                  {'records': records,})
    
@login_required(login_url='dashboard.html')
def dashboard(request):
    '''
    Return dashboard showing general overview of system
    @param request: the HTTP GET request
    @return: rendered dashboard.html
    '''
    
    # Get nodes and gateway statuses
    nodes = Node.objects.all().order_by('node_id')
    gateway_status = False
    gateway_time = None
    node_statuses = []
    for node in nodes:
        if node.get_last_update() is not None:
            node_statuses.append(node.get_last_update())
            gateway_status = True
            gateway_time = node.get_last_update().time_recorded
        else:
            node_statuses.append(node)
    
    # Calculate gaps in existing records
    # Get start range from environmental variable
    start_range = None
    if 'STARTRANGE' not in os.environ:
        os.environ['STARTRANGE'] = str(timezone.datetime.date(
            timezone.datetime.today()))
    start_range = parser.parse(os.environ['STARTRANGE'])
    
    # Make sure environmental variable is still reflecting today's date
    if start_range.day != timezone.now().day:
        start_range = timezone.datetime.date(timezone.datetime.today())
        os.environ['STARTRANGE'] = str(start_range)
        os.environ['DOWNTIME'] = '0'
        
    # Add one day to start range to create end range
    end_range = timezone.timedelta(days=1) + timezone.datetime.date(timezone.now())
    
    print 'Start/End Range', start_range, end_range
    # Retrieve records within start and end range
    records = Record.objects.filter(time_recorded__range=[start_range,
                                                          end_range])
    downtime_counter = 0
    
    # There's new records, check gaps
    if records:
        print 'HAS RECORDS'
        temp = records[0]
        for record in records:
            current = record.time_recorded
            current = current.minute + (current.second / 60) + (current.hour * 60)
            
            temp = temp.time_recorded
            temp = temp.minute + (temp.second / 60) + (temp.hour * 60)
            
            if current - temp > settings.UPDATE_FREQUENCY:
                downtime_counter += current - temp
            
            temp = record
            
        # Calculate gap from last record to now
        temp = temp.time_recorded
        # Get number of minutes in last record
        temp = temp.minute + (temp.second / 60) + (temp.hour * 60)
        # Get number of minutes in current time
        uptime_counter = timezone.now()
        uptime_counter = uptime_counter.minute + (uptime_counter.second / 60) + (uptime_counter.hour * 60)
        # Difference between current and last record > 6, then there's downtime
        if uptime_counter - temp > settings.UPDATE_FREQUENCY:
            downtime_counter += uptime_counter - temp
            gateway_status = False
        # Store new downtime
        if 'DOWNTIME' not in os.environ:
            os.environ['DOWNTIME'] = str(downtime_counter)
        else:
            downtime_counter += int(os.environ['DOWNTIME'])
            os.environ['DOWNTIME'] = str(downtime_counter)
        # Make uptime reflect difference for chart
        uptime_counter = uptime_counter - downtime_counter

    # No new records, check how long we haven't been receiving any
    else:
        print "NO RECORDS"
        current = timezone.now()
        current = current.minute + (current.second / 60) + (current.hour * 60)
        start_range = start_range.minute + (start_range.second / 60) + (start_range.hour * 60)
        if current - start_range > settings.UPDATE_FREQUENCY:
            downtime_counter += current - start_range
            gateway_status = False
        if 'DOWNTIME' not in os.environ:
            os.environ['DOWNTIME'] = str(downtime_counter)
        else:
            downtime_counter += int(os.environ['DOWNTIME'])
            os.environ['DOWNTIME'] = str(downtime_counter)
        uptime_counter = current - downtime_counter

    # Store current time as environmental variable to decrease querysize next
    # request
    os.environ['STARTRANGE'] = str(timezone.now())
   
    return render(request, 'dashboard.html',
                  {'node_status': node_statuses,
                   'gateway_status': gateway_status,
                   'gateway_time': gateway_time,
                   'downtime': downtime_counter,
                   'uptime': uptime_counter,})

@login_required(login_url='login.html')
def node_list(request):
    '''
    Return a list of all Node objects
    @param request: the HTTP GET request
    @return: rendered my_node_list.html containing all Node objects,
    their Sensors, and their Actions
    '''
    nodes = Node.objects.all().order_by('node_id')

    out = []
    for node in nodes:
        sensors = Sensor.objects.filter(node=node).values().order_by('name')
        temp = []
        for s in sensors:
            temp.append(s)
        while len(temp) < 5:
            temp.append(None)
        out.append([node, temp])

    return render(request, 'node_list.html',
                  {'nodes': out,})

@login_required(login_url='login.html')
def admin(request):
    return render(request, 'admin.html')
