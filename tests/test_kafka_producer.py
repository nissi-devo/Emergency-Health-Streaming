import unittest
from unittest.mock import MagicMock
import json
import uuid
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from jobs.helpers.utils import json_serializer
from jobs.kafka_producer import produce_to_kafka

class TestKafkaUtils(unittest.TestCase):
    def test_produce_to_kafka(self):
        producer = MagicMock()
        topic = 'patient_data'
        data = {
            'id': uuid.uuid4(),
            'patient_id': 'IOS-1',
            'heart_rate': 100,
            'timestamp': '2024-07-31T12:00:00'
        }
        produce_to_kafka(producer, topic, data)
        producer.produce.assert_called_once()
        call_args = producer.produce.call_args
        self.assertEqual(call_args[0][0], topic)
        self.assertEqual(call_args[1]['key'], str(data['id']))
        self.assertEqual(call_args[1]['value'], json.dumps(data, default=json_serializer).encode('utf-8'))

if __name__ == '__main__':
    unittest.main()
