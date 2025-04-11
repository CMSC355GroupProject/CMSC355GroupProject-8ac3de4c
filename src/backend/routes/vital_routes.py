# src/backend/routes/vital_routes.py
from flask import Blueprint, jsonify
from dummy_data import get_bpm, get_time, get_spo2, get_ecg, fake_data_generator

vital_bp = Blueprint('vital_bp', __name__)

@vital_bp.route('/vitals', methods=['GET'])
def get_vitals():
    #Generate new data points
    fake_data_generator()

    #Get data from dummy_data
    bpm = get_bpm()
    time = [dt.strftime('%H:%M:%S') for dt in get_time()] # Format time
    spo2 = get_spo2()
    ecg = get_ecg()

    #Return data in JSON format
    return jsonify({
        'bpm_data': bpm,
        'spo2_data': spo2,
        'time_data': time,
        'ecg_data': ecg
    })
