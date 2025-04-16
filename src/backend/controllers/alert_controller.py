from flask import request, jsonify
from bson.objectid import ObjectId
from datetime import datetime
from app import mongo
from models.alert import format_alert
from models.vital import generate_vital_data
from twilio.rest import Client
import os




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
    
    # Validate sensor_type
    sensor_type = data.get("sensor_type")
    allowed_sensor_types = {"BPM", "SPO2", "ECG"}
    if sensor_type not in allowed_sensor_types:
        return jsonify({
            "error": f"Invalid sensor_type: {sensor_type}. Must be one of {list(allowed_sensor_types)}"
        }), 400
    
    # Generate a fresh vitals doc
    vitals = generate_vital_data(patient_obj_id)

    # Pick out the right measured_value
    measured_value = vitals[sensor_type.lower()]

    # Build alert document
    alert = {
        "patient_id": patient_obj_id,
        "sensor_type": data.get("sensor_type"),
        "measured_value": measured_value,
        "threshold_value": data.get("threshold_value"),
        "comparison": data.get("comparison"),
        "timestamp": datetime.utcnow(),
        "message": data.get("message"),
        "is_sent": False,
        "sent_at": None
    }

    # Twilio Configuration
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
    print('Twilio SID: ',TWILIO_ACCOUNT_SID)
    print('Twilio Token: ',TWILIO_AUTH_TOKEN)

    # Add Twilio integration to send alert
    # if alert["is_sent"] == False:
    #     try:
    #         # Initialize Twilio client
    #         client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    #         # Construct the SMS message
    #         message = f"Alert for patient {patient_id}: {alert['sensor_type']} has exceeded threshold! {alert['message']}"

    #         # Send SMS to the patient's contact number
    #         patient_phone = patient.get('phone_number')
    #         if patient_phone:
    #             client.messages.create(
    #                 body=message,
    #                 from_=TWILIO_PHONE_NUMBER,
    #                 to=patient_phone
    #             )
    #             # Update alert to mark as sent
    #             alert["is_sent"] = True
    #             alert["sent_at"] = datetime.utcnow()

    #     except Exception as e:
    #         return jsonify({"error": f"Failed to send SMS: {str(e)}"}), 500
        
    # Insert into DB
    new_id = mongo.db.alerts.insert_one(alert).inserted_id
    new_alert = mongo.db.alerts.find_one({"_id": new_id})

    new_vital = generate_vital_data(patient_obj_id)
    new_vital["timestamp"] = datetime.utcnow()
    mongo.db.vitals.insert_one(new_vital)

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

def update_alert(alert_id):
    print("Inside update_alert route")
    data = request.get_json()

    # Log the incoming data
    print(f"Data received: {data}")

    # Validate ObjectId
    try:
        alert_obj_id = ObjectId(alert_id)
    except Exception as e:
        print(f"Error converting alert_id: {e}")
        return jsonify({"error": "Invalid alert_id"}), 400

    # Log ObjectId conversion
    print(f"alert_id: {alert_id}, alert_obj_id: {alert_obj_id}")

    # Optional: validate allowed fields
    update_fields = {}
    allowed_fields = {"sensor_type", "comparison", "threshold_value", "message"}
    for field in allowed_fields:
        if field in data:
            update_fields[field] = data[field]

    if not update_fields:
        return jsonify({"error": "No valid fields to update"}), 400

    # Log update fields before query
    print(f"Update fields: {update_fields}")

    # Update the alert
    result = mongo.db.alerts.update_one(
        {"_id": alert_obj_id},
        {"$set": update_fields}
    )

    # Log query result
    print(f"Matched count: {result.matched_count}")

    if result.matched_count == 0:
        return jsonify({"error": "Alert not found"}), 404

    updated_alert = mongo.db.alerts.find_one({"_id": alert_obj_id})
    return jsonify(format_alert(updated_alert)), 200
