from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # ✅ Loads config with DB URI
    db.init_app(app)

    # import your routes, models, etc. here

    return app
