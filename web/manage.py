from flask.cli import FlaskGroup

from parser import app
from parser.config import db
from parser.models import Source
from parser.consumer import main
from parser.feed_parse import send_mq, run_parse

cli = FlaskGroup(app)

politic_urls = [
    {
        "name": "Euobserver",
        "url": "https://xml.euobserver.com/rss.xml",
    },
    {
        "name": "Politico",
        "url": "https://rss.politico.com/congress.xml",
    },
    {
        "name": "Reason",
        "url": "https://reason.com/feed/",
    },
]
health_urls = [
    {
        "name": "Politico",
        "url": "https://rss.politico.com/healthcare.xml",
    },
    {
        "name": "WebMD",
        "url": "http://rssfeeds.webmd.com/rss/rss.aspx?RSSSource=RSS_PUBLIC",
    },
    {
        "name": "HealthPhreaks",
        "url": "https://www.healthphreaks.com/feed/",
    },
]
sport_urls = [
    {
        "name": "SportingNews",
        "url": "http://www.sportingnews.com/us/rss",
    },
    {
        "name": "Deadspin",
        "url": "https://deadspin.com/rss",
    },
    {
        "name": "Yardbaker",
        "url": "https://www.yardbarker.com/rss/rumors",
    },
    {
        "name": "Insidesport",
        "url": "https://www.insidesport.in/feed/",
    },
]


@cli.command("load_init_db")
def load_init_db():
    for url in politic_urls:
        s = Source(url=url["url"], name=url["name"], category="politics")
        db.session.add(s)
        db.session.commit()
    for url in health_urls:
        s = Source(url=url["url"], name=url["name"], category="health")
        db.session.add(s)
        db.session.commit()
    for url in sport_urls:
        s = Source(url=url["url"], name=url["name"], category="sport")
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


@cli.command("send_consume")
def send_consume():
    send_mq()


@cli.command("run_parse")
def send_consume():
    run_parse()


if __name__ == "__main__":
    cli()
