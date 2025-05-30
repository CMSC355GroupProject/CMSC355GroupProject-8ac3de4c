from bson.objectid import ObjectId
from app import mongo
from models.vital import generate_vital_data
import threading
import time
from flask import current_app
from datetime import datetime

def create_dummy_vitals(patient_id):
    try:
        patient_obj_id = ObjectId(patient_id)
    except Exception as e:
        return {"error": f"Invalid patient_id: {str(e)}"}, 400

    patient = mongo.db.patients.find_one({"_id": patient_obj_id})
    if not patient:
        return {"error": "Patient not found"}, 404

    vitals_doc = generate_vital_data(patient_obj_id)
    vitals_doc["timestamp"] = datetime.utcnow()  
    insert_result = mongo.db.vitals.insert_one(vitals_doc)

    return {
        "patient_id": str(vitals_doc["patient_id"]),
        "timestamp": vitals_doc["timestamp"].isoformat(),  
        "bpm": vitals_doc["bpm"],
        "spo2": vitals_doc["spo2"],
        "ecg": vitals_doc["ecg"]
    }, 201


def get_latest_vitals(patient_id):
    try:
        patient_obj_id = ObjectId(patient_id)
    except Exception as e:
        return {"error": f"Invalid patient_id: {str(e)}"}, 400

    vitals_doc = mongo.db.vitals.find_one(
        {"patient_id": patient_obj_id},
        sort=[("timestamp", -1)]
    )

    if not vitals_doc:
        print(f"No vitals found for patient_id: {patient_id}") 
        return {"message": "No vitals found for this patient"}, 404

    return {
        "patient_id": str(vitals_doc["patient_id"]),
        "timestamp": vitals_doc["timestamp"],
        "bpm": vitals_doc["bpm"],
        "spo2": vitals_doc["spo2"],
        "ecg": vitals_doc["ecg"]
    }, 200
