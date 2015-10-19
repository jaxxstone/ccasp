from django.test import TestCase
from Receiver.models import Node, Record, Sensor
from datetime import datetime as dt, timedelta
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.contrib.auth.models import User
from django.utils import timezone
from Microcontrollers import settings
class ReceiverTestCase(TestCase):        
    def setUp(self):
        user = User.objects.create_user('temp', 'temp@temp.com', 'temp')
        
    def test_login(self):
        self.assertEqual(self.client.login(username='temp', password='temp'), True)
    
    def test_overview_with_no_values(self):
        self.client.login(username='temp', password='temp')
        response = self.client.get(reverse('records:overview'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['records'], [])
        
    def test_overview_with_values(self):
        Node.objects.create(node_id=999, date_added=dt.now(),name='Test',description='Test')
        Sensor.objects.create(name='TestSensor',node=Node.objects.get(node_id=999),type='Voltage',unit='Watts')
        Record.objects.create(value=50.0, node=Node.objects.get(node_id=999), sensor=Sensor.objects.get(name='TestSensor'))
        
        self.client.login(username='temp', password='temp')
        response = self.client.get(reverse('records:overview'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['records'] is not None)
        
    def test_dashboard(self):
        Node.objects.create(node_id=999, date_added=dt.now(),name='Test',description='Test')
        Sensor.objects.create(name='TestSensor',node=Node.objects.get(node_id=999),type='Voltage',unit='Watts')
        Record.objects.create(value=50.0, node=Node.objects.get(node_id=999), sensor=Sensor.objects.get(name='TestSensor'))
        
        self.client.login(username='temp', password='temp')
        response = self.client.get(reverse('records:dashboard'))
        self.assertEqual(response.status_code, 200)
        
        self.assertTrue(response.context['uptime'] > 0)
        self.assertTrue(response.context['downtime'] >= 0)
        if response.context['downtime'] == 0:
            self.assertTrue(response.context['gateway_status'] == True)
        if response.context['gateway_status'] == True:
            self.assertTrue(timezone.now() - response.context['gateway_time'] <= timedelta(minutes=settings.UPDATE_FREQUENCY))
        else:
            self.assertTrue(timezone.now() - response.context['gateway_time'] > timedelta(minutes=settings.UPDATE_FREQUENCY))
            
    def test_node_list(self):
        Node.objects.create(node_id=999, date_added=dt.now(),name='Test',description='Test')
        Sensor.objects.create(name='TestSensor',node=Node.objects.get(node_id=999),type='Voltage',unit='Watts')
        Record.objects.create(value=50.0, node=Node.objects.get(node_id=999), sensor=Sensor.objects.get(name='TestSensor'))
        
        self.client.login(username='temp', password='temp')
        response = self.client.get(reverse('records:node_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['nodes']) > 0)
        
    def test_admin(self):
        self.client.login(username='temp', password='temp')
        response = self.client.get(reverse('records:node_list'))
        self.assertEqual(response.status_code, 200)

