import os
from confluent_kafka import SerializingProducer
from kafka_producer import simulate_data

#Kafka is exposed on port 9092
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

def main():
    #Set up Kafka producer
    producer_config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'error_cb': lambda err: print(f'Kafka err: {err}')
    }
    producer = SerializingProducer(producer_config)

    try:
        #Generate data
        simulate_data(producer)
    except KeyboardInterrupt:
        print('Patient ended simulation')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')

if __name__ == "__main__":
    main()
