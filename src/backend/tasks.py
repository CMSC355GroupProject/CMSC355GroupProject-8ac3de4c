import os
import time
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

# your model
from models.vital import generate_vital_data

# 1) load .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# 2) connect to MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/rpm")
client = MongoClient(MONGO_URI)
db = client.get_default_database()  # uses the DB in the URI (rpm)

def generate_loop():
    print("Starting vital-generation loop…", flush=True)
    while True:
        patients = db.patients.find()
        for patient in patients:
            new_vital = generate_vital_data(patient["_id"])
            new_vital["timestamp"] = datetime.utcnow()
            db.vitals.insert_one(new_vital)
            print(f"Inserted vital for {patient['_id']}: {new_vital}", flush=True)
        time.sleep(5)

if __name__ == "__main__":
    generate_loop()