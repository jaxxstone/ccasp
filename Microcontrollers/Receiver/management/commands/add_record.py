from Receiver.models import Node, Record
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "adds sample entities to the application"

    def add_arguments(self, parser):
        parser.add_argument('args')

    def handle(self, *args, **options):
        # Get node UUID from arg tuple
        nodeID = int(args[0])
        # Get value from arg tuple
        args = args[1]
                
        # Create float from arg
        out = ''
        for arg in args:
            out += arg
        out = float(out)
        
        # Create new record and add value
        r = Record()
        r.value = out
        
        # Try to match node to existing node
        # objects.get() raises DNE exception if not found
        # Catch and create and save new node with nodeID
        try:
            r.node = Node.objects.get(pk=nodeID)
        except:
            n = Node()
            n.node_id = nodeID
            n.save()
            r.node = n

        print str(r) + " has been added"
        r.save()