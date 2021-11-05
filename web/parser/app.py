from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config.from_object("parser.config.Config")
db = SQLAlchemy(app)


class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, unique=True)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_id = db.Column(db.Integer, db.ForeignKey('source.id'))
    category = db.Column(db.String)
    title = db.Column(db.String)
    published_date = db.Column(db.Date)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now())


@app.route("/")
def index():
    return jsonify(index='index')
