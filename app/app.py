from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app():
    print("got here 0")
    app = Flask(__name__)
    print("got here 1")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    print("got here 2")
    db.init_app(app)
    migrate.init_app(app, db)
    print("got here 3")
    # Import models here
    from app.models.board import Board
    from app.models.card import Card

    # Register Blueprints here
    from .routes import boards_bp
    app.register_blueprint(boards_bp)            

    CORS(app)
    return app