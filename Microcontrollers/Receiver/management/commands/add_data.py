__author__ = 'faculty'

from Receiver.models import Node, Record
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "adds sample entities to the application"

    def handle(self, *args, **options):

        n3 = [3]
        n2 = [2, n3]
        n1 = [1, n3]
        nodes = [n1, n2, n3]

        for node in nodes:
            result = Node(
                          node_id = node[0],
                          )
            result.save()
            
        r1 = [15, 1]
        r2 = [16, 1]
        r3 = [17, 1]
        r4 = [18, 2]
        r5 = [19, 2]
        r6 = [20, 3]
        records = [r1, r2, r3, r4, r5, r6]
        
        for record in records:
            result = Record(
                            value = record[0],
                            node = Node.objects.get(node_id = record[1])
                            )
        