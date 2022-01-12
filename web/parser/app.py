from parser.config import app
from parser.forms import NewsForm
from parser.utils import (
    add_new_source,
    get_statistics_from_db,
    get_statistics_from_files,
    get_today_articles,
)
from typing import Any, Dict, Tuple, Union

from flask import flash, redirect, render_template, request, session

from .feed_parse import run_parse


@app.route("/", methods=["GET"])
def articles_list_get() -> str:
    """Render all articles for today."""
    flash('To start parsing press "Parse Articles"')
    articles, sport_articles = get_today_articles()
    return render_template(
        "article_list.html", articles=articles, sport_articles=sport_articles
    )


@app.route("/", methods=["POST"])
def articles_list_post() -> str:
    """Run articles parsing."""
    run_parse()
    session.pop("_flashes", None)
    flash("Parsing complete!", category="success")
    return redirect("/")


@app.route("/statistics", methods=["GET"])
def statistics() -> str:
    """Render source news statistics."""
    db_statistics = get_statistics_from_db()
    file_statistics = get_statistics_from_files()
    return render_template(
        "statistics.html", db_statistics=db_statistics, file_statistics=file_statistics
    )


@app.route("/add_news", methods=["GET"])
def add_news_get() -> str:
    """Get news source form."""
    form = NewsForm(request.form)
    return render_template("add_news.html", form=form)


@app.route("/add_news", methods=["POST"])
def add_news_post() -> Tuple[Any, int]:
    """Add new news source."""
    form = NewsForm(request.form)
    if form.validate():
        flash_message = add_new_source(form)
        flash(flash_message['message'], category=flash_message['category'])
        return render_template("add_news.html", form=form), 201
    return render_template("add_news.html", form=form)


# API

@app.route("/api/v1/articles-list", methods=["GET"])
def api_articles_list_get() -> dict:
    """Render all articles for today."""
    flash('To start parsing press "Parse Articles"')
    articles, sport_articles = get_today_articles()
    return {
        "articles": list(map(lambda article: article.as_dict(), articles)),
        "sport_articles": list(sport_articles)
    }


@app.route("/api/v1/articles-list", methods=["POST"])
def api_articles_list_post() -> Tuple[Dict[str, str], int]:
    """Run articles parsing."""
    run_parse()
    return {"message": "Start parsing"}, 201


@app.route("/api/v1/statistics", methods=["GET"])
def api_statistics() -> dict:
    """Render source news statistics."""
    db_statistics = get_statistics_from_db()
    file_statistics = get_statistics_from_files()
    return {
        "db_statistics": db_statistics,
        "file_statistics": file_statistics
    }


@app.route("/api/v1/add_news", methods=["POST"])
def api_add_news() -> Tuple[Dict[str, Union[str, dict]], int]:
    """Get news source form."""
    form = NewsForm(
        name=request.json['name'],
        url=request.json['url'],
        source_link=request.json['source_link'],
        category=request.json['category'],
    )
    if form.validate():
        add_new_source(form)
        return {"message": "Form successfully submited!",
                "status": "OK"}, 201
    return {"message": "Form has errors!",
            "status": "FAILED",
            "errors": {
                err[0]: err[1] for err in form.errors.items()
            }}, 204
