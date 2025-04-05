from flask import Blueprint, request
from controllers import auth_controller

auth_bp = Blueprint('auth_bp', __name__)

auth_bp.route('/register', methods=['POST'])(auth_controller.register)
auth_bp.route('/login', methods=['POST'])(auth_controller.login)
