import os
import pathlib

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = pathlib.Path(__file__).parent


class Config():
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
