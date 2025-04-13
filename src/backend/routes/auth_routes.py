from flask import Blueprint, send_from_directory
from controllers import auth_controller
import os

auth_bp = Blueprint('auth_bp', __name__, static_folder='../../frontend')

auth_bp.route('/register', methods=['POST'])(auth_controller.register)
auth_bp.route('/login', methods=['POST'])(auth_controller.login)

