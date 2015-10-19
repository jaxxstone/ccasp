from django.test import TestCase
from Receiver.models import Node, Record, Sensor

class ReceiverTestCase(TestCase):
    def setUp(self):
        Node.objects.create(node_id=999,name='Test',description='Test')
        Sensor.objects.create(name='TestSensor',node=Node.objects.get(node_id=999),type='Voltage',unit='Watts')
        Record.objects.create(value=50.0, node=Node.objects.get(node_id=999), sensor=Sensor.objects.get(name='TestSensor'))
        
    def test_models(self):
        self.assertEqual(1, Node.objects.all().count())
        self.assertEqual(1, Sensor.objects.all().count())
        self.assertEqual(1, Record.objects.all().count())

    def test_node(self):
        node_to_test = Node.objects.get(node_id=999)
        self.assertEqual(1, node_to_test.get_records().count(),
                         'get_records failed')
        self.assertEqual(1, node_to_test.get_most_recent().count(),
                         'get_most_recent failed')
        self.assertEqual(1, node_to_test.get_records_for_today().count(),
                         'get_records_for_today failed')
        self.assertEqual(1, node_to_test.get_records_for_week().count(),
                         'get_records_for_week failed')
        self.assertEqual(1, node_to_test.get_records_for_month().count(),
                         'get_records_for_month failed')
        self.assertEqual(1, node_to_test.get_records_for_year().count(),
                         'get_records_for_year failed')
        
    def test_sensor(self):
        sensor_to_test = Sensor.objects.get(node=Node.objects.get(node_id=999))
        self.assertEqual(1, sensor_to_test.get_records_for_today().count(),
                         'get_records_for_today failed')
        self.assertEqual(1, sensor_to_test.get_records_for_week().count(),
                         'get_records_for_week failed')
        self.assertEqual(1, sensor_to_test.get_records_for_month().count(),
                         'get_records_for_month failed')
        self.assertEqual(1, sensor_to_test.get_records_for_year().count(),
                         'get_records_for_year failed')