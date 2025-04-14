from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from controllers.vital_controller import create_dummy_vitals, get_latest_vitals

vital_bp = Blueprint('vital_bp', __name__)

@vital_bp.route('/', methods=['POST'])
@jwt_required()
def post_vitals():
    jwt_data = get_jwt()
    patient_id = jwt_data.get("patient_id")  # Use claim, not identity
    result, status = create_dummy_vitals(patient_id)
    return jsonify(result), status

@vital_bp.route('/', methods=['GET'])
@jwt_required()
def get_vitals():
    jwt_data = get_jwt()
    print(f"JWT Data: {jwt_data}")  # Check if patient_id is present
    patient_id = jwt_data["patient_id"]
    result, status = get_latest_vitals(patient_id)
    return jsonify(result), status