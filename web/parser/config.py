import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import pathlib

basedir = pathlib.Path(__file__).parent


class Config(object):
    """
    Config for flask project.
    """

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "secret_key"
    WTF_CSRF_ENABLED = True


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
