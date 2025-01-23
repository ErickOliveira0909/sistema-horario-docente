from flask import Flask
import app.manage_key as manage_key
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    chave = manage_key.get_key()
    app.config["SECRET_KEY"] = chave["SECRET_KEY"]
    app.config["SQLALCHEMY_DATABASE_URI"] =  "sqlite:///database.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["PERMENENT_SESSION_LIFETIME"] = timedelta(minutes=60)
    #app.config['SQLALCHEMY_ECHO'] = True
    db.init_app(app)


    from .routes import main
    app.register_blueprint(main)

    return app