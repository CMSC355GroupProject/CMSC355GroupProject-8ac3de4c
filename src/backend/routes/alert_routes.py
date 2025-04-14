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