# app/__init__.py

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient
import os

# Load environment variables
load_dotenv()

# Initialize extensions
bcrypt = Bcrypt()
jwt = JWTManager()
cors = CORS()

def create_app():
    app = Flask(__name__)
    # Load configurations from environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')

    # Initialize extensions with app
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    # Initialize MongoDB client
    client = MongoClient(app.config['MONGO_URI'])
    app.db = client.get_default_database()

    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)

    return app
