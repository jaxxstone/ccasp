'''This module contains the presentation logic for the Receiver application
in the Microcontrollers project. It creates and renders the user-generated
reports, status pages, etc.'''

from django.shortcuts import render
from Receiver.models import Node, Record, Sensor, Action, CompletedAction
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
def daily_report(request, nodeid=None):
    '''
    Return all records from today.
    @param request: the HTTP GET request
    @param nodeid: the Node UUID to generate the report with. Default is None.
    @return: rendered report.html containing a list comprised of Node objects
    and that Node's Sensor values recorded over the past 24 hours
    '''
    time_format = "%Y-%m-%d %H:%M:%S"
    if nodeid:
        nodes = Node.objects.filter(pk=nodeid)
    else:
        nodes = Node.objects.all()

    my_node_list = []
    for node in nodes:
        records = node.get_records_for_today()
        values = []
        for record in records:
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
        my_node_list.append([node.node_id, values])

    return render(request, 'report.html',
                  {'request': request,
                   'node_list': my_node_list,
                   'type': 'Daily',})

@login_required(login_url='login.html')
def weekly_report(request, nodeid=None):
    '''
    Return all records from the past week.
    @param request: the HTTP GET request
    @param nodeid: the Node UUID to generate the report with. Default is None.
    @return: rendered report.html containing a list comprised of Node objects
    and that Node's Sensor values recorded over the past 7 days
    '''
    time_format = "%Y-%m-%d %H:%M:%S"
    my_node_list = []
    if nodeid:
        nodes = Node.objects.filter(pk=nodeid)
    else:
        nodes = Node.objects.all()

    for node in nodes:
        records = node.get_records_for_week()
        values = []
        for record in records:
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
        my_node_list.append([node.node_id, values])

    return render(request, 'report.html',
                  {'request': request,
                   'node_list': my_node_list,
                   'type': 'Weekly',})

@login_required(login_url='login.html')
def monthly_report(request, nodeid=None):
    '''
    Return all records from the past month.
    @param request: the HTTP GET request
    @param nodeid: the Node UUID to generate the report with. Default is None.
    @return: rendered report.html containing a list comprised of Node objects
    and that Node's Sensor values recorded over the past 31 days
    '''
    time_format = "%Y-%m-%d %H:%M:%S"
    my_node_list = []
    if nodeid:
        nodes = Node.objects.filter(pk=nodeid)
    else:
        nodes = Node.objects.all()

    for node in nodes:
        records = node.get_records_for_month()
        values = []
        for record in records:
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
        my_node_list.append([node.node_id, values])

    return render(request, 'report.html',
                  {'request': request,
                   'node_list': my_node_list,
                   'type': 'Monthly',})

@login_required(login_url='login.html')
def yearly_report(request, nodeid=None):
    '''
    Return all records from the past year.
    @param request: the HTTP GET request
    @param nodeid: the Node UUID to generate the report with. Default is None.
    @return: rendered report.html containing a list comprised of Node objects
    and that Node's Sensor values recorded over the past 365 days
    '''
    time_format = "%Y-%m-%d %H:%M:%S"
    my_node_list = []
    if nodeid:
        nodes = Node.objects.filter(pk=nodeid)
    else:
        nodes = Node.objects.all()

    for node in nodes:
        records = node.get_records_for_year()
        values = []
        for record in records:
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
        my_node_list.append([node.node_id, values])

    return render(request, 'report.html',
                  {'request': request,
                   'node_list': my_node_list,
                   'type': 'Yearly',})

@login_required(login_url='login.html')
def custom_form(request, invalid=None):
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
                      {'form': form,})

@login_required(login_url='login.html')
def custom_report(request):
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
    nodes = Node.objects.all()
    for node in nodes:
        records = node.get_records_for_custom(start, end)

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
        my_node_list.append([node.node_id, values])

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
                   'max': end,})

@login_required(login_url='login.html')
def overview(request):
    '''
    Return the 100 most recent Records recorded for all Nodes and Sensors
    @param request: the HTTP GET request
    @return: rendered overview.html containing the Node objects and Records
    '''
    # Get all node objects
    nodes = Node.objects.all()
    # out will hold list of records for each node
    out = Record.objects.all().order_by('-time_recorded')[:100]

    # Return rendered template
    return render(request, 'overview.html',
                  {'records': out,
                   'nodes': nodes,
                   'request': request,})

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
        sensors = Sensor.objects.filter(node=node).values()
        temp = []
        for s in sensors:
            temp.append(s)
        while len(temp) < 5:
            temp.append(None)
        actions = Action.objects.filter(node=node).values()
        out.append([node, temp, actions])

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

@login_required(login_url='login.html')
def get_actions(request):
    '''
    Return a list of scheduled actions
    @param request: the HTTP GET request
    @return: rendered actions.html containing a list of actions
    '''
    actions = Action.objects.all()
    return render(request, 'scheduled_actions.html',
                  {'actions': actions,})

@login_required(login_url='login.html')
def get_recent_actions(request):
    '''
    Return a list of recently executed actions
    @param request: the HTTP GET request
    @return: rendered recent_actions.html containing list of recently
    executed actions
    '''
    actions = CompletedAction.objects.all()
    return render(request, 'recent_actions.html',
                  {'actions': actions,})
