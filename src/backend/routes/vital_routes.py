# src/backend/routes/vital_routes.py
from flask import Blueprint, jsonify
from dummy_data import get_bpm, get_time, fake_data_generator

vital_bp = Blueprint('vital_bp', __name__)

@vital_bp.route('/vitals', methods=['GET'])
def get_vitals():
    # Generate/update data (optional step depending on desired logic)
    fake_data_generator() # Uncomment if you want data generation on each request

    bpm = get_bpm()
    time = [dt.strftime('%H:%M:%S') for dt in get_time()] # Format time

    # Return data in JSON format expected by the frontend
    return jsonify({
        'bpm_data': bpm,
        'time_data': time
    })
