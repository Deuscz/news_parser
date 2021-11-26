from parser import app
from parser.config import db
from parser.consumer import main
from parser.models import Source

from flask.cli import FlaskGroup

cli = FlaskGroup(app)

INIT_DATA = {"politics": [  # Init politic sources
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
], "health": [  # Init health sources
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
], "sport": [  # Init sport sources
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
]}


@cli.command("load_init_db")
def load_init_db():
    """Init database sources."""
    sources = []
    for category, urls in INIT_DATA.items():
        for url in urls:
            sources.append(Source(
                url=url["url"],
                name=url["name"],
                source_link=url["source_link"],
                category=category,
            ))
    db.session.add_all(sources)
    db.session.commit()


@cli.command("create_db")
def create_db():
    """Create database tables."""
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("start_consume")
def start_consume():
    """Start script in consumer container."""
    main()


if __name__ == "__main__":
    cli()
