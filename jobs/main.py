import os

from confluent_kafka import SerializingProducer
from config import configuration
from kafka_producer import simulate_data

#Define environment variables
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

if __name__ == "__main__":

    producer_config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'error_cb': lambda err: print(f'Kafka err: {err}')
    }
    producer = SerializingProducer(producer_config)

    try:
        simulate_data(producer)
    except KeyboardInterrupt:
            print('Patient ended simulation')
    except Exception as e:
            print(f'An unexpected error occurred: {e}')