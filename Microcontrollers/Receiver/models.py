from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Node(models.Model):
    '''
    Node model represents an end node
    '''
    # UUID
    node_id = models.IntegerField(primary_key = True)
    # Date and time that node first came online
    date_added = models.DateTimeField(default=timezone.now)
    # Label assigned by user
    name = models.CharField(max_length = 75, null=True)
        
    def __str__(self):
        '''
        Override default string behavior
        '''
        return "Node " + str(self.node_id)
    
    def get_records(self):
        '''
        Returns all Record objects associated with the node
        @return: a list of Record objects associated with the node
        '''
        return Record.objects.filter(node = self)
    
    def get_most_recent(self):
        '''
        Returns 20 most recent Record objects
        @return: a list of Record objects
        '''
        return Record.objects.all().order_by('time_recorded')[:20]
            
    def get_records_for_today(self):
        '''
        Return records from the past 24 hours
        @return: a list of Record objects for this node recorded in the past 24 hours
        '''
        today = timezone.now()
        date_from = today - timezone.timedelta(days=1)
        return Record.objects.filter(node = self, time_recorded__gte = date_from)
    
    def get_records_for_week(self):
        '''
        Return records from the past 7 days
        @return: a list of Record objects for this node recorded in the past 7 days
        '''
        today = timezone.now()
        date_from = today - timezone.timedelta(days=7)
        return Record.objects.filter(node = self, time_recorded__gte = date_from)
    
    def get_records_for_month(self):
        '''
        Return records from the past 31 days
        @return: a list of Record objects for this node recorded in the past 31 days
        '''
        today = timezone.now()
        date_from = today - timezone.timedelta(days=31)
        return Record.objects.filter(node = self, time_recorded__gte = date_from)
    
    def get_records_for_year(self):
        '''
        Return records from the past 365 days
        @return: a list of Record objects for this node recorded in the past 365 days
        '''
        today = timezone.now()
        date_from = today - timezone.timedelta(days=365)
        return Record.objects.filter(node = self, time_recorded__gte = date_from)
    
    def get_records_for_custom(self, start, end):
        '''
        Return records from custom date range
        @param start: the starting datetime
        @param end: the ending datetime
        @return: a list of Record objects for this node recorded in the specified time period
        '''
        return Record.objects.filter(node = self, time_recorded__gte = start, time_recorded__lte = end)
    
        
class Record(models.Model):
    '''
    Record model represents a reading returned by a Node's Sensor 
    '''
    # Value recorded
    value = models.FloatField()
    # Node that returned this record
    node = models.ForeignKey(Node)
    # Time that the record was recorded
    time_recorded = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        '''
        Override default string behavior
        '''
        return "Node " + str(self.node.node_id) + ": " + str(self.value)    

class Sensor(models.Model):
    '''
    Sensor model represents a Sensor attached to a Node
    '''
    # Name assigned to Sensor by user
    name = models.CharField(max_length = 75, null = True)
    # Node that this Sensor belongs to
    node = models.ForeignKey(Node)
    
    def __str__(self):
        '''
        Override default string behavior
        '''
        return "Node " + str(self.node.node_id) + " " + self.name + " Sensor"
    
	# Took a stab at limiting number of sensors per node
	# Commenting out for now
	'''
    def save(self):
        if Sensor.objects.filter(node = self.node).count() >= 5:
            return
        else:
            super(Sensor, self).save()
            
    def clean(self):
        if Sensor.objects.filter(node = self.node).count() > 5:
            raise ValidationError("Cannot add more than five sensors per node")
        else:
            super(Sensor, self).clean()
	'''

class Action(models.Model):
    '''
    TODO: Finish
    Action model represents a user-defined action to be performed by a node or sensor at a specified time
    '''
    # User-provided name of the Action
    name = models.CharField(max_length = 75, null = True)
    # Node associated with the Action
    node = models.ForeignKey(Node)
    
    def __str__(self):
        '''
        Override default string behavior
        '''
        return "Node " + str(self.node.node_id) + ": " + str(self.name)
