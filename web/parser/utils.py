from datetime import datetime
from parser.models import Article, Source

from sqlalchemy import desc


def reformat_str_data(date: str, format_from: str, format_to: str) -> str:
    """Rеformats string date to another format."""
    date = datetime.strptime(date, format_from).date()
    return date.strftime(format_to)


def date_to_str(date: datetime, format_to: str = "%Y-%m-%d") -> str:
    """Converts datetime object to sting."""
    return date.strftime(format_to)


def get_statistics_from_db() -> list:
    """Returns statistics from database."""
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
            Source.source_link == s.source_link,
        ):
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
            if num_of_health_articles == 0 and len(health_articles) != 0:
                num_of_health_articles = len(health_articles)
            elif num_of_politics_articles == 0 and len(politics_articles) != 0:
                num_of_politics_articles = len(politics_articles)
            last_news_date = (
                Article.query.filter(Article.url_id == source.id)
                .order_by(desc(Article.published_date))
                .first()
            )
            if last_news_date and source.category == "health":
                last_health_date = date_to_str(last_news_date.published_date)
            elif last_news_date and source.category == "politics":
                last_politics_date = date_to_str(last_news_date.published_date)
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
