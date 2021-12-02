import logging
import os
import pathlib

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

logging.basicConfig(filename='error.log', level=logging.ERROR)
basedir = pathlib.Path(__file__).parent


class Config:
    """Developer config for flask project."""

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "secret_key"
    WTF_CSRF_ENABLED = True
    DEBUG = True


class TestConfig(Config):
    """Test config for flask project."""

    WTF_CSRF_ENABLED = False


# Project configs
configs = {
    "dev": Config,
    "test": TestConfig,
}

app = Flask(__name__)
app.config.from_object(configs[os.getenv("CONFIG", default="dev")])
db = SQLAlchemy(app)
