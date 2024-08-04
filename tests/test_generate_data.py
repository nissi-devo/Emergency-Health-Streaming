import unittest
import sys
import os
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from jobs.kafka_producer import generate_patient_data, generate_emergency_vehicle_data

class TestKafkaProducer(unittest.TestCase):
    def test_generate_patient_data(self):
        data = generate_patient_data()
        self.assertIn('id', data)
        self.assertIn('patient_id', data)
        self.assertIn('heart_rate', data)
        self.assertIn('oxygen_saturation', data)
        self.assertIn('vo2_max', data)
        self.assertIn('location', data)
        self.assertIn('emergency_alert', data)
        self.assertIn('timestamp', data)
        self.assertIsInstance(data['id'], uuid.UUID)
        self.assertTrue(50 <= data['heart_rate'] <= 200)
        self.assertTrue(80 <= data['oxygen_saturation'] <= 100)
        self.assertTrue(15 <= data['vo2_max'] <= 50)
        self.assertIsInstance(data['timestamp'], str)

    def test_generate_emergency_vehicle_data(self):
        data = generate_emergency_vehicle_data()
        self.assertIn('id', data)
        self.assertIn('vehicle_id', data)
        self.assertIn('vehicle_type', data)
        self.assertIn('vehicle_capacity', data)
        self.assertIn('location', data)
        self.assertIn('patient_id', data)
        self.assertIn('dispatch_time', data)
        self.assertIn('timestamp', data)
        self.assertIsInstance(data['id'], uuid.UUID)
        self.assertIsInstance(data['dispatch_time'], str)
        self.assertIsInstance(data['timestamp'], str)

if __name__ == '__main__':
    unittest.main()
