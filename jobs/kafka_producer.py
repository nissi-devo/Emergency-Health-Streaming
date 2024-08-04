import os
import sys
import time
from datetime import datetime, timedelta
import random
import uuid

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from jobs.helpers.utils import produce_to_kafka

#Specify two topics for kafka stream
PATIENT_TOPIC = os.getenv('PATIENT_TOPIC', 'patient_data')
EMERGENCY_VEHICLE_TOPIC = os.getenv('EMERGENCY_TOPIC', 'emergency_vehicle_data')
def generate_patient_data():
    #Generate random data indicating patient vital signs within believable ranges
    os_type = random.choice(["IOS", "ANDROID"])
    patient_data = {
        "id": uuid.uuid4(),
        "patient_id": f"{os_type}-{random.randint(1, 20)}",
        "heart_rate": random.randint(50, 200),
        "oxygen_saturation": random.uniform(80, 100),
        "vo2_max": random.uniform(15, 50),
        "location": {
            "latitude": random.uniform(51.509865, 51.519865),
            "longitude": random.uniform(-0.118092, -0.128092)
        },
        "emergency_alert": random.choice([True, False]),  # Randomly simulate emergency alerts
        "timestamp": datetime.now().isoformat()
    }
    return patient_data

def generate_emergency_vehicle_data(vehicle_type="Ambulance"):
    #Simulate vehicle categories
    vehicle_types = [
        {"type": "Ambulance", "capacity": "Basic Life Support"},
        {"type": "Ambulance", "capacity": "Advanced Life Support"},
        {"type": "Ambulance", "capacity": "Intensive Care Unit"}
    ]
    #Filter for ambulances
    filtered_vehicle_types = [v for v in vehicle_types if v["type"] == vehicle_type]

    vehicle_info = random.choice(filtered_vehicle_types)
    os_type = random.choice(["IOS", "ANDROID"])
    v_categ = random.choice(["BLS", "ALS", "ICU"])

    dispatch_time = datetime.now()
    #Define believable range for arrival time
    arrival_time_offset = random.uniform(5, 30)  # Random offset between 5 and 15 minutes
    arrival_time = dispatch_time + timedelta(minutes=arrival_time_offset)

    # Generate random emergency vehicle data within believable ranges
    vehicle_data = {
        "id": uuid.uuid4(),
        "vehicle_id": f"{v_categ}-{random.randint(1, 20)}",
        "vehicle_type": vehicle_info["type"],
        "vehicle_capacity": vehicle_info["capacity"],
        "location": {
            "latitude": random.uniform(51.509865, 51.519865),
            "longitude": random.uniform(-0.118092, -0.128092)
        },
        "patient_id": f"{os_type}-{random.randint(1, 20)}",
        "dispatch_time": dispatch_time.isoformat(),
        "timestamp": arrival_time.isoformat()
    }
    return vehicle_data

def simulate_data(producer):
    while True:
        #generate data
        patient_data = generate_patient_data()
        emergency_data = generate_emergency_vehicle_data()

        print("Starting to produce to kafka..")

        #send data to kafka stream
        produce_to_kafka(producer, PATIENT_TOPIC, patient_data)
        produce_to_kafka(producer, EMERGENCY_VEHICLE_TOPIC, emergency_data)

        time.sleep(1)  # Simulate real-time data with 1 second intervals