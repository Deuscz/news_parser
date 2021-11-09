import datetime
from flask import Flask, jsonify
from parser.config import db, app
from .feed_parse import run_parse
import asyncio

@app.route("/")
def index():
    run_parse()
    return jsonify(index="index")
