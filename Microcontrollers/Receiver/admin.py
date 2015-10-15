''' This module contains the presentation logic for the Admin panel used by
the Microcontrollers application.'''
# pylint: disable=too-many-public-methods, no-value-for-parameter, no-member

from django.contrib import admin
from Receiver.models import Node, Record, Sensor

class RecordInline(admin.TabularInline):
    '''
    Admin panel inline view for Record objects
    @param admin.TabularInline: Django template for inline views
    '''
    model = Record
    extra = 0

class SensorAdmin(admin.ModelAdmin):
    model = Sensor
    extra = 0
    ordering = ('node',)

class SensorInline(admin.TabularInline):
    '''
    Admin panel inline view for Sensor objects
    @param admin.TabularInline: Django template for inline views
    '''
    model = Sensor
    extra = 0

    def has_add_permission(self, request):
        '''
        Attempt to limit number of Sensors, doesn't work yet
        @param request: the HTTP request
        '''
        num_objects = self.model.objects.count()
        if num_objects >= 5:
            return False
        else:
            return True

class NodeAdmin(admin.ModelAdmin):
    '''
    Admin panel model view for Node objects
    @param admin.ModelAdmin: Django template for model views
    '''
    model = Node
    inlines = [SensorInline,]
    ordering = ('node_id',)

admin.site.register(Node, NodeAdmin)
admin.site.register(Sensor, SensorAdmin)
