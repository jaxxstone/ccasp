from django.contrib import admin
from Receiver.models import Node, Record, Sensor
# Register your models here.


class RecordInline(admin.TabularInline):
    model = Record
    extra = 0

class SensorInline(admin.TabularInline):
    model = Sensor
    extra = 0

    def has_add_permission(self, request):
        num_objects = self.model.objects.count()
        if num_objects >= 5:
            return False
        else:
            return True

class NodeAdmin(admin.ModelAdmin):
    model = Node
    inlines = [SensorInline]
    ordering = ('node_id',)

admin.site.register(Node, NodeAdmin)