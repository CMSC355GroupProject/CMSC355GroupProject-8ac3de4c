from flask import request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime
from app import mongo

def is_valid_dob_format(dob_str):
    try:
        datetime.strptime(dob_str, "%m-%d-%Y")
        return True
    except ValueError:
        return False
    
def register():
    data = request.get_json()

    required_fields = ["username", "email", "password", "dob", "height", "weight", "biological_gender", "phone_number"]
    missing = [field for field in required_fields if field not in data]

    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    # Check DOB format
    if not is_valid_dob_format(data["dob"]):
        return jsonify({"error": "DOB must be in MM-DD-YYYY format"}), 400
    
    # Check if username exists
    existingUsername = mongo.db.patients.find_one({"username": data["username"]})
    if existingUsername:
        print(f"User already registered with username: {data['username']}", flush=True)
        return jsonify({"error": "Username already in use"}), 409

    # Check if email exists
    existingEmail = mongo.db.patients.find_one({"email": data["email"]})
    if existingEmail:
        print(f"User already registered with email: {data['email']}", flush=True)
        return jsonify({"error": "Email already registered"}), 409

    data["password"] = generate_password_hash(data["password"])
    mongo.db.patients.insert_one(data)
    return jsonify({ "message": "User registered successfully" }), 201

def login():
    data = request.get_json()
    user = mongo.db.patients.find_one({ "email": data["email"] })
    if not user or not check_password_hash(user["password"], data["password"]):
        return jsonify({ "error": "Invalid credentials" }), 401

    token = jwt.encode({
        "user_id": str(user["_id"]),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }, current_app.config["SECRET_KEY"], algorithm="HS256")

    return jsonify({ "token": token })
