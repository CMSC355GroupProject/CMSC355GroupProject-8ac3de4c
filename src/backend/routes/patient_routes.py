from flask import Blueprint
from controllers import patient_controller

patient_bp = Blueprint('patient_bp', __name__)

# /api/patient prefix
patient_bp.route('/', methods=['GET'])(patient_controller.get_all_patients)
patient_bp.route('/', methods=['POST'])(patient_controller.create_patient)
patient_bp.route('/current', methods=['GET'])(patient_controller.get_current_patient)