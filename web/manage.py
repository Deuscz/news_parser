from parser import app
from parser.config import db
from parser.consumer import main
from parser.feed_parse import run_parse
from parser.models import Source

from flask.cli import FlaskGroup

cli = FlaskGroup(app)

politic_urls = [
    {
        "name": "Euobserver",
        "source_link": "https://euobserver.com/",
        "url": "https://xml.euobserver.com/rss.xml",
    },
    {
        "name": "Politico",
        "source_link": "https://www.politico.com/",
        "url": "https://rss.politico.com/congress.xml",
    },
    {
        "name": "Reason",
        "source_link": "https://reason.com/",
        "url": "https://reason.com/feed/",
    },
]
health_urls = [
    {
        "name": "Politico",
        "source_link": "https://www.politico.com/",
        "url": "https://rss.politico.com/healthcare.xml",
    },
    {
        "name": "WebMD",
        "source_link": "https://www.webmd.com/",
        "url": "http://rssfeeds.webmd.com/rss/rss.aspx?RSSSource=RSS_PUBLIC",
    },
    {
        "name": "HealthPhreaks",
        "source_link": "https://www.healthphreaks.com/",
        "url": "https://www.healthphreaks.com/feed/",
    },
]
sport_urls = [
    {
        "name": "SportingNews",
        "source_link": "https://www.sportingnews.com/",
        "url": "http://www.sportingnews.com/us/rss",
    },
    {
        "name": "Deadspin",
        "source_link": "https://deadspin.com/",
        "url": "https://deadspin.com/rss",
    },
    {
        "name": "Yardbaker",
        "source_link": "https://www.yardbarker.com/",
        "url": "https://www.yardbarker.com/rss/rumors",
    },
    {
        "name": "Insidesport",
        "source_link": "https://www.insidesport.in/",
        "url": "https://www.insidesport.in/feed/",
    },
]


@cli.command("load_init_db")
def load_init_db():
    for url in politic_urls:
        s = Source(
            url=url["url"],
            name=url["name"],
            source_link=url["source_link"],
            category="politics",
        )
        db.session.add(s)
        db.session.commit()
    for url in health_urls:
        s = Source(
            url=url["url"],
            name=url["name"],
            source_link=url["source_link"],
            category="health",
        )
        db.session.add(s)
        db.session.commit()
    for url in sport_urls:
        s = Source(
            url=url["url"],
            name=url["name"],
            source_link=url["source_link"],
            category="sport",
        )
        db.session.add(s)
        db.session.commit()


@cli.command("create_db")
def create_db():
    """
    Creating database
    :return:
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("start_consume")
def start_consume():
    main()


@cli.command("run_parse")
def send_consume():
    run_parse()


if __name__ == "__main__":
    cli()
