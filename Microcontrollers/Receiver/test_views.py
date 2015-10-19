from django.test import TestCase
from Receiver.models import Node, Record, Sensor
from datetime import timedelta
import datetime
from django.core.urlresolvers import reverse
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
        Node.objects.create(node_id=999, name='Test',description='Test')
        Sensor.objects.create(name='TestSensor',node=Node.objects.get(node_id=999),type='Voltage',unit='Watts')
        Record.objects.create(value=50.0, node=Node.objects.get(node_id=999), sensor=Sensor.objects.get(name='TestSensor'))
        
        self.client.login(username='temp', password='temp')
        response = self.client.get(reverse('records:overview'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['records'] is not None)
        
    def test_dashboard(self):
        Node.objects.create(node_id=999, name='Test',description='Test')
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
            
        self.assertTrue(type(response.context['downtime']) is int)
        self.assertTrue(type(response.context['uptime']) is int)
        self.assertTrue(type(response.context['gateway_time']) is datetime.datetime)
        self.assertTrue(type(response.context['gateway_status']) is bool)
        self.assertTrue(type(response.context['node_status']) is list)
        
    def test_node_list(self):
        self.client.login(username='temp', password='temp')
        response = self.client.get(reverse('records:node_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['nodes']) == 0)
        Node.objects.create(node_id=999, name='Test',description='Test')
        response = self.client.get(reverse('records:node_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['nodes']) == 1)
        
    def test_admin(self):
        self.client.login(username='temp', password='temp')
        response = self.client.get(reverse('records:node_list'))
        self.assertEqual(response.status_code, 200)

    def test_daily_report(self):
        test_node = Node.objects.create(node_id=999, name='Test',description='Test')
        test_sensor = Sensor.objects.create(name='TestSensor',node=Node.objects.get(node_id=999),type='Voltage',unit='Watts')
        Record.objects.create(value=50.0, node=Node.objects.get(node_id=999), sensor=Sensor.objects.get(name='TestSensor'))

        self.client.login(username='temp', password='temp')
        response = self.client.get(reverse('records:daily_report', args=[test_node.node_id, test_sensor.id]))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('records:daily_report', args=[test_node.node_id]))
        self.assertEqual(response.status_code, 404)