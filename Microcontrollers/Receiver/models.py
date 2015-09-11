from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Node(models.Model):
    # UUID
    node_id = models.IntegerField(primary_key = True)
    # Date and time that node first came online
    date_added = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length = 75, null=True)
    
    # Return neighboring nodes
    def get_neighbors(self):
        return self.objects.filter(neighbors = self.node_id)
    
    # Return UUID as string
    def __str__(self):
        return "Node " + str(self.node_id)
    
    # Get all records for Node
    def get_records(self):
        return Record.objects.filter(node = self)
    
    def get_most_recent(self):
        return Record.objects.all().order_by('time_recorded')[:20]
            
    def get_records_for_today(self):
        '''
        Return records from the past 24 hours
        '''
        today = timezone.now()
        date_from = today - timezone.timedelta(days=1)
        return Record.objects.filter(node = self, time_recorded__gte = date_from)
    
    def get_records_for_week(self):
        '''
        Return records from the past 7 days
        '''
        today = timezone.now()
        date_from = today - timezone.timedelta(days=7)
        return Record.objects.filter(node = self, time_recorded__gte = date_from)
    
    def get_records_for_month(self):
        '''
        Return records from the past 7 days
        '''
        today = timezone.now()
        date_from = today - timezone.timedelta(days=31)
        return Record.objects.filter(node = self, time_recorded__gte = date_from)
    
    def get_records_for_year(self):
        '''
        Return records from the past 7 days
        '''
        today = timezone.now()
        date_from = today - timezone.timedelta(days=365)
        return Record.objects.filter(node = self, time_recorded__gte = date_from)
    
    def get_records_for_custom(self, start, end):
        '''
        Return records from custom date range
        @param start: the starting datetime
        @param end: the ending datetime
        '''
        return Record.objects.filter(node = self, time_recorded__gte = start, time_recorded__lte = end)
    
        
class Record(models.Model):
    # Value recorded
    value = models.FloatField()
    # Node that returned this record
    node = models.ForeignKey(Node)
    # Time that the record was recorded
    time_recorded = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return "Node " + str(self.node.node_id) + ": " + str(self.value)    

class Sensor(models.Model):
    name = models.CharField(max_length = 75, null = True)
    node = models.ForeignKey(Node)
    
    def __str__(self):
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
    name = models.CharField(max_length = 75, null = True)
    node = models.ForeignKey(Node)
    
    def __str__(self):
        return "Node " + str(self.node.node_id) + ": " + str(self.name)
