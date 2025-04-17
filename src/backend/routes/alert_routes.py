from flask import Blueprint
from controllers import alert_controller

alert_bp = Blueprint('alert_bp', __name__)

# /api/alerts prefix

@alert_bp.route('/', methods=['POST'])
def create_alert():
    return alert_controller.create_alert()

@alert_bp.route('/', methods=['GET'])
def get_alerts():
    return alert_controller.get_alerts()

@alert_bp.route('/<alert_id>', methods=['PUT'])
def update_alert(alert_id):
    print("Inside update_alert route")
    return alert_controller.update_alert(alert_id)

@alert_bp.route('/<alert_id>', methods=['DELETE'])
def delete_alert(alert_id):
    return alert_controller.delete_alert(alert_id)