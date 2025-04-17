from flask import request, jsonify
from bson.objectid import ObjectId
from app import mongo
from models.patient import format_patient
from flask_jwt_extended import jwt_required, get_jwt
from pymongo import ReturnDocument

def get_all_patients():
    patients = mongo.db.patients.find()
    return jsonify([format_patient(p) for p in patients])

def create_patient():
    data = request.get_json()
    new_id = mongo.db.patients.insert_one(data).inserted_id
    new_patient = mongo.db.patients.find_one({"_id": new_id})
    return jsonify(format_patient(new_patient)), 201

@jwt_required()
def get_current_patient():
    claims = get_jwt()
    patient_id = claims.get("patient_id") 

    if not patient_id:
        return jsonify({"error": "Patient ID not found in token"}), 400

    patient = mongo.db.patients.find_one({"_id": ObjectId(patient_id)})
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    return jsonify(format_patient(patient)), 200

def convert_objectid(data):
    if isinstance(data, dict):
        return {key: convert_objectid(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_objectid(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    return data

@jwt_required()
def update_patient():
    claims = get_jwt()  
    patient_id = claims.get("patient_id")  

    if not patient_id:
        return jsonify({"error": "Patient ID is missing from token"}), 400

    try:
        patient_id = ObjectId(patient_id)  
    except Exception as e:
        return jsonify({"error": "Invalid patient ID format"}), 400

    print(f"Updating patient with ID: {patient_id}")

    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    updated_patient = mongo.db.patients.find_one_and_update(
        {"_id": patient_id},  
        {"$set": data},  
        return_document=ReturnDocument.AFTER
    )

    if updated_patient:
        updated_patient = convert_objectid(updated_patient)
        return jsonify(updated_patient), 200  
    else:
        print(f"Patient with ID {patient_id} not found or update failed.")
        return jsonify({"error": "Patient not found or update failed"}), 404  