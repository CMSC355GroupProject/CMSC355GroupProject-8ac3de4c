from flask import Flask, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token
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

    # Validate input
    if 'email' not in data or 'password' not in data:
        return jsonify({"error": "Email and password are required"}), 400

    email = data["email"]
    password = data["password"]

    # Check if the user exists in the database
    user = mongo.db.patients.find_one({"email": email})
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401  # Unauthorized

    # Compare hashed passwords
    if not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid email or password"}), 401

    # Generate a token (if using JWT for session)
    access_token = create_access_token(identity=user["email"])

    return jsonify({
        "message": "Login successful",
        "access_token": access_token
    }), 200
