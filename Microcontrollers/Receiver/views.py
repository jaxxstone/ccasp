from django.shortcuts import render
from Receiver.models import Node, Record, Sensor, Action
from Receiver.forms import CustomReport
import serial
import time
import json
from django.utils import timezone
from Microcontrollers.settings import TTY_PORT
from datetime import datetime as dt, datetime
from django.core.management import call_command
from StringIO import StringIO
from django.contrib.auth.decorators import login_required

@login_required(login_url='login.html')
def report_list(request):
    '''
    Generates a list of Nodes and the report types (daily, weekly, etc.) available
    @param request: the HTTP GET request
    @return: rendered report_list.html with a list of Node objects
    '''
    nodes = Node.objects.all()
    return render(request, 'report_list.html',
                  {'nodes': nodes }
                  )

@login_required(login_url='login.html')
def daily_report(request, nodeid = None):
    '''
    Return all records from today.
    @param request: the HTTP GET request
    @param nodeid: the Node UUID to generate the report with. Default is None.
    @return: rendered report.html containing a list comprised of Node objects and that Node's
    Sensor values recorded over the past 24 hours
    '''
    timeFormat = "%Y-%m-%d %H:%M:%S"
    
    node_list = []
    if nodeid:
        nodes = Node.objects.filter(pk = nodeid)
    else:
        nodes = Node.objects.all()
        
    for node in nodes:
        records = node.get_records_for_today()
        
        values = []
        for record in records:
            # Get time that record was added
            myTime = record.time_recorded
            # Format time as string
            myTime = myTime.strftime(timeFormat)
            # Convert to Epoch time (in ms) for Highcharts
            myTime = int(dt.strptime(myTime, timeFormat).strftime('%s')) * 1000    
            # Append to list
            # Highcharts requires [time, value] format for datetime graph
            values.append([myTime, record.value])
        
        # Add node and sensor values list to main list
        node_list.append([node.node_id, values])
        
    return render(request, 'report.html', 
                              {'request': request,
                              'node_list': node_list,
                              'type': 'Daily',
                              })

@login_required(login_url='login.html')
def weekly_report(request, nodeid = None):
    '''
    Return all records from the past week.
    @param request: the HTTP GET request
    @param nodeid: the Node UUID to generate the report with. Default is None.
    @return: rendered report.html containing a list comprised of Node objects and that Node's
    Sensor values recorded over the past 7 days
    '''
    timeFormat = "%Y-%m-%d %H:%M:%S"
    
    node_list = []
    if nodeid:
        nodes = Node.objects.filter(pk = nodeid)
    else:
        nodes = Node.objects.all()
        
    for node in nodes:
        records = node.get_records_for_week()
        
        values = []
        for record in records:
            # Get time that record was added
            myTime = record.time_recorded
            # Format time as string
            myTime = myTime.strftime(timeFormat)
            # Convert to Epoch time (in ms) for Highcharts
            myTime = int(dt.strptime(myTime, timeFormat).strftime('%s')) * 1000    
            # Append to list
            # Highcharts requires [time, value] format for datetime graph
            values.append([myTime, record.value])
        
        # Add node and sensor values list to main list
        node_list.append([node.node_id, values])
    return render(request, 'report.html', 
                              {'request': request,
                              'node_list': node_list,
                              'type': 'Weekly',
                              }
                              )

@login_required(login_url='login.html')
def monthly_report(request, nodeid = None):
    '''
    Return all records from the past month.
    @param request: the HTTP GET request
    @param nodeid: the Node UUID to generate the report with. Default is None.
    @return: rendered report.html containing a list comprised of Node objects and that Node's
    Sensor values recorded over the past 31 days
    '''
    timeFormat = "%Y-%m-%d %H:%M:%S"
    
    node_list = []
    if nodeid:
        nodes = Node.objects.filter(pk = nodeid)
    else:
        nodes = Node.objects.all()
        
    for node in nodes:
        records = node.get_records_for_month()
        
        values = []
        for record in records:
            # Get time that record was added
            myTime = record.time_recorded
            # Format time as string
            myTime = myTime.strftime(timeFormat)
            # Convert to Epoch time (in ms) for Highcharts
            myTime = int(dt.strptime(myTime, timeFormat).strftime('%s')) * 1000    
            # Append to list
            # Highcharts requires [time, value] format for datetime graph
            values.append([myTime, record.value])
        
        # Add node and sensor values list to main list
        node_list.append([node.node_id, values])
    return render(request, 'report.html', 
                              {'request': request,
                              'node_list': node_list,
                              'type': 'Monthly',
                              }
                              )

@login_required(login_url='login.html')
def yearly_report(request, nodeid = None):
    '''
    Return all records from the past year.
    @param request: the HTTP GET request
    @param nodeid: the Node UUID to generate the report with. Default is None.
    @return: rendered report.html containing a list comprised of Node objects and that Node's
    Sensor values recorded over the past 365 days
    '''
    timeFormat = "%Y-%m-%d %H:%M:%S"
    
    node_list = []
    if nodeid:
        nodes = Node.objects.filter(pk = nodeid)
    else:
        nodes = Node.objects.all()
        
    for node in nodes:
        records = node.get_records_for_year()
        
        values = []
        for record in records:
            # Get time that record was added
            myTime = record.time_recorded
            # Format time as string
            myTime = myTime.strftime(timeFormat)
            # Convert to Epoch time (in ms) for Highcharts
            myTime = int(dt.strptime(myTime, timeFormat).strftime('%s')) * 1000    
            # Append to list
            # Highcharts requires [time, value] format for datetime graph
            values.append([myTime, record.value])
        
        # Add node and sensor values list to main list
        node_list.append([node.node_id, values])
    return render(request, 'report.html', 
                              {'request': request,
                              'node_list': node_list,
                              'type': 'Yearly',
                              }
                              )

@login_required(login_url='login.html')
def custom_form(request, invalid = None, nodeid = None):
    '''
    Returns a form used to generate a custom report
    @param request: the HTTP GET request
    @param invalid: Boolean value indicating whether the start and end datetime ranges are valid
    @param nodeid: the Node UUID to generate the report with. Default is None.
    @return: rendered custom.html containing a CustomReport form model. Returns an invalid flag if there were errors.
    '''
    if request.method == 'GET':
        form = CustomReport()
        
    if invalid:
        return render(request, 'custom.html',
                  {'form': form,
                   'error': True,
                   }
                  )
    else:
        return render(request, 'custom.html',
                  {'form': form,
                   }
                  )

@login_required(login_url='login.html')
def custom_report(request):
    '''
    Returns the custom report requested by the user
    @param request: the HTTP GET request
    @return: rendered report.html containing a list comprised of Node objects and that Node's
    Sensor values recorded over the requested time period 
    '''
    # Retrieve dates and times from request
    startDate = request.GET['startDate']
    startTime = request.GET['startTime']
    endDate = request.GET['endDate']
    endTime = request.GET['endTime']
    offset = request.GET['tzOffset']
    
    # Convert offset minutes to ms
    offset = int(offset) * 60 * 1000
    
    # string format for time
    timeFormat = '%Y-%m-%d %H:%M'
    startString = startDate + ' ' + startTime 
    endString = endDate + ' ' + endTime
    
    # Create new datetime from strings
    start = timezone.datetime.strptime(startString, timeFormat)
    end = timezone.datetime.strptime(endString, timeFormat)
        
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
    node_list = []
    nodes = Node.objects.all()
    for node in nodes:
        records = node.get_records_for_custom(start, end)
        
        values = []
        for record in records:
            # Get time that record was added
            myTime = record.time_recorded
            # Format time as string
            myTime = myTime.strftime(timeFormat)
            # Convert to Epoch time for Highcharts
            myTime = int(dt.strptime(myTime, timeFormat).strftime('%s')) * 1000    
            # Append to list
            # Highcharts requires [time, value] format for datetime graph
            values.append([myTime, record.value])
        
        # Add node and sensor values list to main list
        node_list.append([node.node_id, values])
        
    # Convert start and end to Epoch time for chart ranges
    start = start.strftime(timeFormat)
    start = int(dt.strptime(start, timeFormat).strftime('%s')) * 1000
    end = end.strftime(timeFormat)
    end = int(dt.strptime(end, timeFormat).strftime('%s')) * 1000
    
    return render(request, 'report.html', 
                              {'request': request,
                              'node_list': node_list,
                              'type': 'Custom Range',
                              'min': json.dumps(start),
                              'max': end,
                              }
                              )

@login_required(login_url='login.html')
def overview(request):
    '''
    Return the 20 most recent Records recorded for all Nodes and Sensors
    @param request: the HTTP GET request
    @return: rendered overview.html containing the Node objects and Records
    '''    
    # Get all node objects
    nodes = Node.objects.all()
    # out will hold list of records for each node
    out = Record.objects.all().order_by('-time_recorded')[:20]
            
    # Return rendered template
    return render(request, 'overview.html', 
                              {'records': out,
                              'nodes': nodes,
                              'request': request,}
                              )

@login_required(login_url='login.html')
def node_list(request):
    '''
    Return a list of all Node objects
    @param request: the HTTP GET request
    @return: rendered node_list.html containing all Node objects, their Sensors, and their Actions
    '''
    nodes = Node.objects.all()    
    
    out = []
    for node in nodes:
        sensors = Sensor.objects.filter(node = node)
        actions = Action.objects.filter(node = node)
        out.append([node, sensors, actions])
        
    return render(request, 'node_list.html',
                  {'nodes': out,}
                  )

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
    #call_command('get_node_status', nodeid, stdout=out)
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
                   'node': node,}
                  )
