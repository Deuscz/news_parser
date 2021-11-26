from parser.config import app
from parser.forms import NewsForm
from parser.utils import (
    add_new_source,
    get_statistics_from_db,
    get_statistics_from_files,
    get_today_articles,
)

from flask import flash, redirect, render_template, request, session

from .feed_parse import run_parse


@app.route("/", methods=["GET", "POST"])
def articles_list() -> str:
    """Render all articles for today."""
    flash('To start parsing press "Parse Articles"')
    if request.method == "POST":
        run_parse()
        session.pop("_flashes", None)
        flash("Parsing complete!", category="success")
        return redirect("/")
    articles, sport_articles = get_today_articles()
    return render_template(
        "article_list.html", articles=articles, sport_articles=sport_articles
    )


@app.route("/statistics", methods=["GET"])
def statistics() -> str:
    """Render source news statistics."""
    db_statistics = get_statistics_from_db()
    file_statistics = get_statistics_from_files()
    return render_template(
        "statistics.html", db_statistics=db_statistics, file_statistics=file_statistics
    )


@app.route("/add_news", methods=["GET", "POST"])
def add_news() -> str:
    """View to add new news source."""
    form = NewsForm(request.form)
    if request.method == "POST":
        if form.validate():
            flash_message = add_new_source(form)
            flash(flash_message['massage'], category=flash_message['category'])
            return render_template("add_news.html", form=form), 201
    return render_template("add_news.html", form=form)
