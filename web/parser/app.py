import datetime
from flask import Flask, jsonify
from parser.config import db, app
from .feed_parse import run_parse
from parser.models import Source, Article

@app.route("/")
def index():
    run_parse()
    articles = Article.query.filter_by(published_date=datetime.date.today())
    return jsonify([article.as_dict() for article in articles])
