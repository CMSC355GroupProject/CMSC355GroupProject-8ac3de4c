def format_alert(alert_doc):
    return {
        "id": str(alert_doc["_id"]),
        "patient_id": str(alert_doc["patient_id"]),
        "sensor_type": alert_doc.get("sensor_type"),
        "measured_value": alert_doc.get("measured_value"),
        "threshold_value": alert_doc.get("threshold_value"),
        "comparison": alert_doc.get("comparison"),
        "timestamp": alert_doc.get("timestamp"),
        "message": alert_doc.get("message"),
        "is_sent": alert_doc.get("is_sent"),
        "sent_at": alert_doc.get("sent_at"),
    }