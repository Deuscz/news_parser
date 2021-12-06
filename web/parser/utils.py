import datetime
import json
from os import listdir
from os.path import isfile, join
from parser.config import app, db
from parser.forms import NewsForm
from parser.models import Article, Source
from typing import Dict, List, Tuple, Union

from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError, PendingRollbackError

DATE_FORMATS = [  # Formats for date parser
    "%a, %d %b %Y %H:%M:%S",
    "%a, %d %B %Y %H:%M:%S",
    "%a %d %b %Y %H:%M:%S",
    "%d %b %Y %H:%M:%S",
]


def reformat_str_data(date: str, format_from: str, format_to: str) -> str:
    """Reformat string date to another format.

    Args:
        date: date string
        format_from: format string from
        format_to: format string to
    Returns:
        formatted date
    """
    date = datetime.datetime.strptime(date, format_from).date()
    return date.strftime(format_to)


def date_to_str(date: datetime.datetime, format_to: str = "%Y-%m-%d") -> str:
    """Convert datetime object to sting.

    Args:
        date: datetime object
        format_to: format string
    Returns:
        formatted date
    """
    return date.strftime(format_to)


def get_date_from_feed(date: str) -> datetime.datetime:
    """Get date from rss article feed string.

    Args:
        date: date string
    Returns:
        published data in datetime format
    """
    published_date = ''
    for date_format in DATE_FORMATS:
        try:
            published_date = datetime.datetime.strptime(" ".join(date.split(" ")[:-1]), date_format).date()
        except ValueError:
            # skipping wrong date formats
            continue
    if not published_date:
        published_date = datetime.datetime.today()
    return published_date


def get_articles_data_from_feed(articles: List) -> List[Article]:
    """Get articles data from rss feed.
    Args:
        article[0]:news url_id
        article[1]:news category
        article[2]:news title
        article[3]:news published date
    Returns:
        list of articles
    """
    data = []
    for article in articles:
        published_date = get_date_from_feed(article[3])
        if published_date == datetime.date.today():
            data.append(
                {
                    "url_id": article[0],
                    "category": article[1],
                    "title": article[2],
                    "published_date": published_date.strftime("%Y-%m-%d"),
                }
            )
    return data


def articles_list_by_category(source: Source, category: str) -> List[Article]:
    """Get list of articles by category name.

    Args:
        source: source of article
        category: category name
    Returns:
        list of articles
    """
    return list(Article.query.filter(Article.url_id == source.id, Article.category == category))


def get_number_of_articles(health_articles: List[Article], politics_articles: List[Article],
                           num_of_health_articles: int,
                           num_of_politics_articles: int) -> Tuple[int, int]:
    """Calculate number of articles in list.

    Args:
        health_articles: list of articles with category health
        politics_articles: list of articles with category politics
        num_of_health_articles: number of health articles
        num_of_politics_articles: number of politics articles
    Returns:
        tuple of ints with number of articles by category
    """

    if num_of_health_articles == 0 and len(health_articles) != 0:
        num_of_health_articles = len(health_articles)
    elif num_of_politics_articles == 0 and len(politics_articles) != 0:
        num_of_politics_articles = len(politics_articles)
    return num_of_health_articles, num_of_politics_articles


def get_last_articles_date(source: Source, last_health_date: str, last_politics_date: str) -> Tuple[str, str]:
    """Get last articles date by source.

    Args:
        source: source of articles
        last_health_date: last health date string
        last_politics_date: last politics date string
    Returns:
        tuple of strings with last dates of articles by source
    """
    last_news_date = (
        Article.query.filter(Article.url_id == source.id).order_by(desc(Article.published_date)).first()
    )
    if last_news_date and source.category == "health":
        last_health_date = date_to_str(last_news_date.published_date)
    elif last_news_date and source.category == "politics":
        last_politics_date = date_to_str(last_news_date.published_date)
    return last_health_date, last_politics_date


def get_statistics_from_db() -> List[Dict]:
    """Return statistics from database.

    Returns:
        list with database articles statistics
    """
    num_of_health_articles = num_of_politics_articles = last_health_date = last_politics_date = ''
    db_statistics = []
    for s in Source.query.filter(Source.category.in_(("health", "politics"))).distinct(
            Source.source_link
    ):
        num_of_health_articles = 0
        num_of_politics_articles = 0
        last_health_date = ""
        last_politics_date = ""
        for source in Source.query.filter(
                Source.category.in_(("health", "politics")),
                Source.source_link == s.source_link, ):
            health_articles = articles_list_by_category(source, category="health")
            politics_articles = articles_list_by_category(source, category="politics")
            num_of_health_articles, num_of_politics_articles = get_number_of_articles(health_articles,
                                                                                      politics_articles,
                                                                                      num_of_health_articles,
                                                                                      num_of_politics_articles)
            last_health_date, last_politics_date = get_last_articles_date(source, last_health_date, last_politics_date)
        db_statistics.append(
            {
                "source_url": s.source_link,
                "health_articles": num_of_health_articles,
                "politics_articles": num_of_politics_articles,
                "last_news_date": last_health_date
                if last_health_date > last_politics_date
                else last_politics_date,
            }
        )
    return db_statistics


def get_statistics_from_files() -> Union[Dict[str, Union[int, str]], Dict]:
    """Return statistics from files.

    Returns:
        dict with sport files statistics
    """
    try:
        # get list of files in sport_files directory
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
    except Exception as ex:
        # return empty dict if exception
        file_statistics = {}
        app.logger.error(ex)
    return file_statistics


def get_articles_from_file(date: datetime.datetime = datetime.datetime.today()) -> List[Dict]:
    """Get list of sport articles from file.

    Args:
        date: datetime object
    Returns:
        list of sport articles
    """
    try:
        filename = "sport_" + date.strftime("%Y-%m-%d") + ".txt"
        with open("sport_files/" + filename, "r", encoding="UTF-8") as f:
            sport_articles = json.load(f)
            for article in sport_articles:
                source = Source.query.filter_by(id=article["url_id"]).first()
                article["source_name"] = source.name
                article["url"] = source.source_link
    except OSError:
        sport_articles = []
    return sport_articles


def get_articles_from_db() -> List[Article]:
    """Return today`s articles from db.

    Returns:
        list of articles
    """

    articles = Article.query.join(Source).filter(
        Article.published_date == datetime.date.today()
    )
    return articles


def get_today_articles() -> Tuple[List[Article], List[Article]]:
    """Return all articles.

    Returns:
        tuple of all articles
    """
    return get_articles_from_db(), get_articles_from_file()


def add_new_source(form: NewsForm) -> Dict[str, str]:
    """Add new news source to database.

    Args:
        form: data to commit
    Returns:
        dict with message and category for flash
    """

    try:
        source = Source(
            name=form.name.data,
            url=form.url.data,
            source_link=form.source_link.data,
            category=form.category.data,
        )
        db.session.add(source)
        db.session.commit()
        return {"message": "Source was added successfully!", "category": "success"}
    except (IntegrityError, PendingRollbackError):
        db.session.rollback()
        return {"message": "Source is already in database!", "category": "alert"}
