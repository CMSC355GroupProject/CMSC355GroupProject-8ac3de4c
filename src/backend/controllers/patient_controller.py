from flask import request, jsonify
from bson.objectid import ObjectId
from app import mongo
from models.patient import format_patient
from flask_jwt_extended import jwt_required, get_jwt_identity

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
    current_user_email = get_jwt_identity()
    patient = mongo.db.patients.find_one({"email": current_user_email})
    if not patient:
        return jsonify({"error": "Patient not found"}), 404
    return jsonify(format_patient(patient)), 200