'''This module contains the business logic for the Receiver application
in the Microcontrollers project. It defines the objects used to represent
Nodes, Sensors, Actions, and Records, and is used by Django to create the ORM
database.'''
# pylint: disable=no-value-for-parameter, no-member

from django.db import models
from django.utils import timezone

class Node(models.Model):
    '''Node model represents an end node'''
    # UUID
    node_id = models.IntegerField(primary_key=True)
    # Date and time that node first came online
    date_added = models.DateTimeField(default=timezone.now)
    # Label assigned by user
    name = models.CharField(max_length=75, null=True,
                            help_text="Add a descriptive name to uniquely identify this node.")
    description = models.CharField(max_length=200, null=True,
                                   help_text="Add a description to help identify this node (location, purpose, etc.).")

    def __str__(self):
        '''Override default string behavior'''
        if self.name:
            return "Node %s %s" % (self.node_id, self.name)
        else:
            return "Node %s" % self.node_id

    def __unicode__(self):
        if self.name:
            return "Node %s %s" % (self.node_id, self.name)
        else:
            return "Node %s" % self.node_id

    def get_records(self):
        '''
        Returns all Record objects associated with the node
        @return: a list of Record objects associated with the node
        '''
        return Record.objects.filter(node=self)

    def get_most_recent(self):
        '''
        Returns 20 most recent Record objects
        @return: a list of Record objects
        '''
        return Record.objects.all().order_by('time_recorded')[:20]

    def get_records_for_today(self):
        '''
        Return records from the past 24 hours
        @return: a list of Record objects for this node recorded in the past
        24 hours
        '''
        today = timezone.now()
        date_from = today - timezone.timedelta(days=1)
        return Record.objects.filter(node=self,
                                     time_recorded__gte=date_from)

    def get_records_for_week(self):
        '''
        Return records from the past 7 days
        @return: a list of Record objects for this node recorded in the past
        7 days
        '''
        today = timezone.now()
        date_from = today - timezone.timedelta(days=7)
        return Record.objects.filter(node=self,
                                     time_recorded__gte=date_from)

    def get_records_for_month(self):
        '''
        Return records from the past 31 days
        @return: a list of Record objects for this node recorded in the past
        31 days
        '''
        today = timezone.now()
        date_from = today - timezone.timedelta(days=31)
        return Record.objects.filter(node=self,
                                     time_recorded__gte=date_from)

    def get_records_for_year(self):
        '''
        Return records from the past 365 days
        @return: a list of Record objects for this node recorded in the past
        365 days
        '''
        today = timezone.now()
        date_from = today - timezone.timedelta(days=365)
        return Record.objects.filter(node=self,
                                     time_recorded__gte=date_from)

    def get_records_for_custom(self, start, end):
        '''
        Return records from custom date range
        @param start: the starting datetime
        @param end: the ending datetime
        @return: a list of Record objects for this node recorded in the
        specified time period
        '''
        return Record.objects.filter(node=self, time_recorded__gte=start,
                                     time_recorded__lte=end)
        
    def get_last_update(self):
        return Record.objects.filter(node=self).last()

class Record(models.Model):
    '''Record model represents a reading returned by a Node's Sensor'''
    # Value recorded
    value = models.FloatField()
    # Node that returned this record
    node = models.ForeignKey(Node)
    # Sensor that returned this record
    sensor = models.ForeignKey('Sensor', null=True)
    # Time that the record was recorded
    time_recorded = models.DateTimeField(default=timezone.now)

    def __str__(self):
        '''Override default string behavior'''
        return "Node " + str(self.node.node_id) + ": " + str(self.value)

class Sensor(models.Model):
    '''Sensor model represents a Sensor attached to a Node'''
    # Name assigned to Sensor by user
    name = models.CharField(max_length=75, null=True)
    # Node that this Sensor is associated with
    node = models.ForeignKey(Node)
    # Type of sensor
    sensor_choices = (('Air Temperature', 'Air Temperature'), 
                      ('Humidity', 'Humidity'),
                      ('Soil Moisture', 'Soil Moisture'),
                      ('Rain', 'Rain'),
                      ('Voltage', 'Voltage'))
    sensor_units = (('C', 'Celcius'),
                    ('F', 'Fahrenheit'),
                    ('%', '%'),
                    ('in', 'Inches'),
                    ('cm', 'Centimeters'),
                    ('W', 'Watts'))
    type = models.CharField(max_length=50,
                            choices=sensor_choices,
                            null=True,
                            help_text="Select a type of sensor from the above list.")
    unit = models.CharField(max_length=50,
                            choices=sensor_units,
                            null=True,
                            help_text="Select a unit of measurement for this type of sensor. This measurement will be used when reporting and graphing the output of this sensor.")

    def __str__(self):
        '''Override default string behavior'''
        return "Node " + str(self.node.node_id) + " " + self.name + " Sensor"

    def get_records_for_today(self):
        '''
        Return records from the past 24 hours
        @return: a list of Record objects for this sensor recorded in the past
        24 hours
        '''
        today = timezone.now()
        date_from = today - timezone.timedelta(days=1)
        return Record.objects.filter(sensor=self,
                                     time_recorded__gte=date_from)

    def get_records_for_week(self):
        '''
        Return records from the past 7 days
        @return: a list of Record objects for this sensor recorded in the past
        7 days
        '''
        today = timezone.now()
        date_from = today - timezone.timedelta(days=7)
        return Record.objects.filter(sensor=self,
                                     time_recorded__gte=date_from)

    def get_records_for_month(self):
        '''
        Return records from the past 31 days
        @return: a list of Record objects for this sensor recorded in the past
        31 days
        '''
        today = timezone.now()
        date_from = today - timezone.timedelta(days=31)
        return Record.objects.filter(sensor=self,
                                     time_recorded__gte=date_from)

    def get_records_for_year(self):
        '''
        Return records from the past 365 days
        @return: a list of Record objects for this sensor recorded in the past
        365 days
        '''
        today = timezone.now()
        date_from = today - timezone.timedelta(days=365)
        return Record.objects.filter(sensor=self,
                                     time_recorded__gte=date_from)

    def get_records_for_custom(self, start, end):
        '''
        Return records from custom date range
        @param start: the starting datetime
        @param end: the ending datetime
        @return: a list of Record objects for this sensor recorded in the
        specified time period
        '''
        return Record.objects.filter(sensor=self, time_recorded__gte=start,
                                     time_recorded__lte=end)