from flask import request, jsonify
from bson.objectid import ObjectId
from datetime import datetime
from app import mongo
from models.alert import format_alert

# POST: Create an alert
def create_alert():
    data = request.get_json()

    # Validate patient ID
    patient_id = data.get("patient_id")
    if not patient_id:
        return jsonify({"error": "Missing patient_id"}), 400

    try:
        patient_obj_id = ObjectId(patient_id)
    except:
        return jsonify({"error": "Invalid patient_id"}), 400

    # Make sure patient exists
    patient = mongo.db.patients.find_one({"_id": patient_obj_id})
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    # Build alert document
    alert = {
        "patient_id": patient_obj_id,
        "sensor_type": data.get("sensor_type"),
        "measured_value": data.get("measured_value"),
        "threshold_value": data.get("threshold_value"),
        "comparison": data.get("comparison"),
        "timestamp": datetime.utcnow(),
        "message": data.get("message"),
        "is_sent": False,
        "sent_at": None
    }

    # Add Twilio integration to send alert (your Twilio code here)

    # Insert into DB
    new_id = mongo.db.alerts.insert_one(alert).inserted_id
    new_alert = mongo.db.alerts.find_one({"_id": new_id})
    return jsonify(format_alert(new_alert)), 201


# GET: Retrieve alerts
def get_alerts():
    # Get query parameters
    patient_id = request.args.get('patient_id')
    sensor_type = request.args.get('sensor_type')
    is_sent = request.args.get('is_sent')

    # Build filter for Mongo query
    filters = {}
    if patient_id:
        try:
            filters["patient_id"] = ObjectId(patient_id)
        except:
            return jsonify({"error": "Invalid patient_id"}), 400

    if sensor_type:
        filters["sensor_type"] = sensor_type

    if is_sent is not None:
        try:
            filters["is_sent"] = bool(int(is_sent))  # Convert to boolean
        except ValueError:
            return jsonify({"error": "Invalid value for is_sent. Use 0 or 1."}), 400

    # Fetch alerts from MongoDB based on the filters
    alerts_cursor = mongo.db.alerts.find(filters)
    
    # Convert alerts to a list of formatted alert responses
    alerts = [format_alert(alert) for alert in alerts_cursor]

    if not alerts:
        return jsonify({"message": "No alerts found matching the criteria."}), 404

    return jsonify(alerts), 200