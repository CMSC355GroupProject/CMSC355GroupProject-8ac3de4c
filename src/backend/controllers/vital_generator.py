from datetime import datetime
from models.vital import generate_vital_data
from app import mongo

def generate_vitals_for_all():
    try:
        patients = mongo.db.patients.find()
        patient_count = mongo.db.patients.count_documents({})  # Use count_documents to get the number of patients
        print(f"Found {patient_count} patients.")  # Log the number of patients
        for patient in patients:
            print(f"Generating vital data for patient: {patient['_id']}")
            new_vital = generate_vital_data(patient["_id"])
            print(f"Generated new vital data: {new_vital}")
            new_vital["timestamp"] = datetime.utcnow()
            mongo.db.vitals.insert_one(new_vital)
            print(f"Inserted new vital for patient: {patient['_id']}")
    except Exception as e:
        print(f"Error generating vitals for all: {e}", flush=True)
        raise  # Reraise the exception to ensure it's caught in the Flask route
