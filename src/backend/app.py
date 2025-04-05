from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

mongo = PyMongo()

# JWT Secret Key
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/rpm")
    app.config["SECRET_KEY"] = SECRET_KEY
    mongo.init_app(app)

    # Import and register Blueprints
    from routes.auth_routes import auth_bp
    from routes.patient_routes import patient_bp
    from routes.vital_routes import vital_bp
    from routes.alert_routes import alert_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(patient_bp, url_prefix="/api/patient")
    app.register_blueprint(vital_bp, url_prefix="/api/vitals")
    app.register_blueprint(alert_bp, url_prefix="/api/alerts")

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
