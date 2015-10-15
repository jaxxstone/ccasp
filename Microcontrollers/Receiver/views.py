'''This module contains the presentation logic for the Receiver application
in the Microcontrollers project. It creates and renders the user-generated
reports, status pages, etc.'''

from django.shortcuts import render
from Receiver.models import Node, Record, Sensor
from Receiver.forms import CustomReport
import json
from django.utils import timezone
from datetime import datetime as dt
from django.core.management import call_command
from StringIO import StringIO
from django.contrib.auth.decorators import login_required

@login_required(login_url='login.html')
def report_list(request):
    '''
    Generates a list of Nodes and the report types (daily, weekly, etc.)
    available
    @param request: the HTTP GET request
    @return: rendered report_list.html with a list of Node objects
    '''
    nodes = Node.objects.all()
    return render(request, 'report_list.html',
                  {'nodes': nodes})

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
                   'sensor_unit': sensor_unit,})

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
                   'sensor_unit': sensor_unit,})

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
                   'sensor_unit': sensor_unit,})

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
                   'sensor_unit': sensor_unit,})

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
    type = sensor.type
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
                   'type': 'Custom Range',
                   'min': json.dumps(start),
                   'max': end,
                   'sensor_type': type,
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
    nodes = Node.objects.all().order_by('node_id')
    gateway_status = False
    node_statuses = []
    for node in nodes:
        if node.get_last_update() is not None:
            node_statuses.append(node.get_last_update())
            gateway_status = True
        else:
            node_statuses.append(node)
    return render(request, 'dashboard.html',
                  {'node_status': node_statuses,
                   'gateway_status': gateway_status,})

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
def node_status(request, nodeid):
    '''
    Return whether the given node is online
    TODO: Implement
    @param request: the HTTP GET request
    @param nodeid: the Node UUID to check
    @return: rendered node_status.html containing the Node and its online status
    '''
    # Commented out "Test" button behavior for now
    # Capture management command return from stdout
    #out = StringIO()
    #call_command('get_node_status', nodeid, stdout = out)
    #status = out.getvalue()
    status = 0
    #try:
    #    status = int(status)
    #except:
    #    pass

    node = Node.objects.get(pk=nodeid)
    online = False
    if status == 1:
        online = True

    return render(request, 'node_status.html',
                  {'status': online,
                   'node': node,})