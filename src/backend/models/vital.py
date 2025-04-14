from datetime import datetime
import random

def generate_vital_data(patient_id):
    return {
        "patient_id": patient_id,
        "timestamp": datetime,
        "bpm": random.randint(60, 100),
        "spo2": random.randint(90, 100),
        "ecg": round(random.uniform(0.5, 1.5), 2)
    }