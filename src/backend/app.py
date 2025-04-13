from flask import Flask, render_template
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()

mongo = PyMongo()
jwt   = JWTManager()

def create_app():
    app = Flask(__name__,
            static_folder='../frontend/assets',  # Folder with your static files
            template_folder='../frontend')
    
    CORS(app)

    app.config["MONGO_URI"]      = os.getenv("MONGO_URI", "mongodb://localhost:27017/rpm")
    app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SECRET_KEY"]     = app.config["JWT_SECRET_KEY"]

    mongo.init_app(app)
    jwt.init_app(app)

    print(f"Secret key from .env: {app.config['JWT_SECRET_KEY']}", flush=True)

    @app.route('/')
    def login():
        return render_template('login.html')

    from routes.auth_routes    import auth_bp
    from routes.patient_routes import patient_bp
    from routes.vital_routes   import vital_bp
    from routes.alert_routes   import alert_bp

    app.register_blueprint(auth_bp,    url_prefix="/api/auth")
    app.register_blueprint(patient_bp, url_prefix="/api/patient")
    app.register_blueprint(vital_bp,   url_prefix="/api/vitals")
    app.register_blueprint(alert_bp,   url_prefix="/api/alerts")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)