import datetime
from flask import Flask, jsonify, request, render_template, redirect
from parser.config import db, app
from .feed_parse import run_parse
from parser.models import Source, Article
from parser.utils import reformat_str_data
import json
from os import listdir
from os.path import isfile, join
from sqlalchemy import desc


@app.route("/articles_list", methods=["GET"])
def articles_list():
    articles = Article.query.join(Source).filter(
        Article.published_date == datetime.date.today()
    )
    try:
        filename = "sport_" + datetime.date.today().strftime("%Y-%m-%d") + ".txt"
        with open("sport_files/" + filename, "r") as f:
            sport_articles = json.load(f)
            for article in sport_articles:
                source = Source.query.filter_by(id=article["url_id"]).first()
                article["source_name"] = source.name
                article["url"] = source.url
    except OSError:
        sport_articles = []
    return render_template(
        "article_list.html", articles=articles, sport_articles=sport_articles
    )


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        run_parse()
        return redirect("/")
    return render_template("index.html")


@app.route("/statistics", methods=["GET"])
def statistics():
    db_statistics = []
    for source in Source.query.filter(Source.category.in_(("health", "politics"))):
        health_articles = list(
            Article.query.filter(
                Article.url_id == source.id, Article.category == "health"
            )
        )
        politics_articles = list(
            Article.query.filter(
                Article.url_id == source.id, Article.category == "politics"
            )
        )
        last_news_date = (
            Article.query.filter(Article.url_id == source.id)
            .order_by(desc(Article.published_date))
            .first()
        )
        if last_news_date:
            db_statistics.append(
                {
                    "source_url": source.url,
                    "health_articles": len(health_articles),
                    "politics_articles": len(politics_articles),
                    "last_news_date": last_news_date.published_date,
                }
            )

    try:
        files = [
            f.split("_")[1][:-4]
            for f in listdir("sport_files")
            if isfile(join("sport_files", f))
        ]
        number_of_files = len(files)
        min_date = reformat_str_data(min(files), "%Y-%m-%d", "%-d %b %Y")
        max_date = reformat_str_data(max(files), "%Y-%m-%d", "%-d %b %Y")
        file_statistics = {
            "number_of_files": number_of_files,
            "min_date": min_date,
            "max_date": max_date,
        }
    except:
        file_statistics = {}
    return render_template(
        "statistics.html", db_statistics=db_statistics, file_statistics=file_statistics
    )
