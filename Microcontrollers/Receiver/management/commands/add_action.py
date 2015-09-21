'''This module is used by the jobs.py script to instantiate a CompletedAction object
received by the cron job and add it to the database'''
# pylint: disable=no-value-for-parameter, no-member

from Receiver.models import Node, Record
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    '''Default class for Django's management commands'''
    help = "adds a new CompletedAction to the database"

    def add_arguments(self, parser):
        parser.add_argument('args')

    def handle(self, *args, **options):
        # Get IDs from arg tuple
        job_id = int(args[0])

        # Create CompletedAction object
        completed_action = CompletedAction()
        
        # Retrieve Action object matching job ID
        try:
            action = Action.objects.get(pk=job_id)
            completed_action.action = action
        except:
            completed_action.action = None

        completed_action.status = True
        completed_action.time = dt.now()
        completed_action.save()
