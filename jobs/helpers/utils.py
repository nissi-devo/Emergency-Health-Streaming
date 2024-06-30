import json
import uuid


def json_serializer(obj): #To handle the serialization of Python objects to JSON, specifically for objects of type uuid.UUID
    if isinstance(obj, uuid.UUID):
        return str(obj)
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')
def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed due to: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}')
def produce_to_kafka(producer, topic, data): #Callback function that handles the delivery report for Kafka messages.
        producer.produce(
            topic,
            key=str(data['id']),
            value=json.dumps(data, default=json_serializer).encode('utf-8'),
            on_delivery=delivery_report
        )
        producer.flush()
