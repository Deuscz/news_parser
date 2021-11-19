import datetime
from flask import Flask, jsonify, request, render_template, redirect, flash, session
from parser.config import db, app
from .feed_parse import run_parse
from parser.models import Source, Article
from parser.forms import NewsForm
from parser.utils import get_statistics_from_db, reformat_str_data
from sqlalchemy.exc import IntegrityError, PendingRollbackError
import json
from os import listdir
from os.path import isfile, join


@app.route("/", methods=["GET", "POST"])
def articles_list() -> str:
    """
    Render all articles for today.
    """
    flash('To start parsing press "Parse Articles"')
    if request.method == "POST":
        run_parse()
        session.pop("_flashes", None)
        flash("Parsing complete!", category="success")
        return redirect("/")
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
                article["url"] = source.source_link
    except OSError:
        sport_articles = []
    return render_template(
        "article_list.html", articles=articles, sport_articles=sport_articles
    )


@app.route("/statistics", methods=["GET"])
def statistics() -> str:
    """
    Render source news statistics.
    """
    db_statistics = get_statistics_from_db()
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


@app.route("/add_news", methods=["GET", "POST"])
def add_news() -> str:
    """
    View to add new news source.
    """
    form = NewsForm(request.form)
    if request.method == "POST":
        if form.validate():
            try:

                source = Source(
                    name=form.name.data,
                    url=form.url.data,
                    source_link=form.source_link.data,
                    category=form.category.data,
                )
                db.session.add(source)
                db.session.commit()
                flash("Source was added successfully!", category="success")
            except (IntegrityError, PendingRollbackError):
                db.session.rollback()
                flash("Source is already in database!")
        return render_template("add_news.html", form=form)
    return render_template("add_news.html", form=form)
