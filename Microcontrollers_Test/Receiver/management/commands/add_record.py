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
        # Get node UUID from arg tuple
        node_id = int(args[0])
        # Get value from arg tuple
        args = args[1]

        # Create float from arg
        out = ''
        for arg in args:
            out += arg
        out = float(out)

        # Create new record and add value
        new_record = Record()
        new_record.value = out
        try:
            new_record.sensor = Sensor.objects.get(pk=node_id)
        except:
            new_sensor = Sensor()
            new_sensor.node = Node.objects.get(pk=1)
            new_sensor.name = "Auto Add"
            new_sensor.save()
            new_record.sensor = new_sensor

        print str(new_record.sensor) + " has been added"

        # Try to match node to existing node
        # objects.get() raises DNE exception if not found
        # Catch and create and save new node with nodeID
        try:
            new_record.node = Node.objects.get(pk=1)
        except:
            new_node = Node()
            new_node.node_id = node_id
            new_node.save()
            new_record.node = new_node

        print str(new_record) + " has been added"
        new_record.save()
