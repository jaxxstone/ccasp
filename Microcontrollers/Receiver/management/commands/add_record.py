'''This module is used by the read_data.py script to instantiate a Record object
from received serial data and add it to the database.'''
# pylint: disable=no-value-for-parameter, no-member

from Receiver.models import Node, Record, Sensor
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    '''Default class for Django's management commands'''
    help = "adds a new Record to the database"
    
    def add_arguments(self, parser):
        parser.add_argument('args')

    def handle(self, *args, **options):
        # Lookups for sensor pin number
        types = {'14': 'Temperature', '15': 'Humidity', '16': 'Soil Moisture'}
        units = {'14': 'C', '15': '%', '16': '%'}
        
        # Get node UUID from arg tuple
        sensor_id = str(args[0])
        # Get value from arg tuple
        value = args[1]
        
        # Create new record and add value
        new_record = Record()
        new_record.value = value

        try:
            new_record.sensor = Sensor.objects.get(pk=sensor_id)
        except:
            new_sensor = Sensor()
            new_sensor.pk = sensor_id
            new_sensor.node = Node.objects.get(pk=1)
            new_sensor.name = types[sensor_id]
            new_sensor.type = types[sensor_id]
            new_sensor.unit = units[sensor_id]
            new_sensor.save()
            new_record.sensor = new_sensor
            print "Sensor " + str(new_record.sensor) + " has been added"

        # Try to match node to existing node
        # objects.get() raises DNE exception if not found
        # Catch and create and save new node with nodeID
        try:
            new_record.node = Node.objects.get(pk=1)
        except:
            new_node = Node()
            new_node.node_id = 1
            new_node.save()
            new_record.node = new_node

        print str(new_record.sensor.name) + " " + str(new_record.value) + " has been added"
        new_record.save()

    def convert_to_fahr(self, temperature):
        temperature = (float(temperature) * (9.0/5.0)) + 32.0
        temperature = str(temperature)
        return temperature
