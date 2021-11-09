from flask.cli import FlaskGroup

from parser import app
from parser.config import db
from parser.models import Source

cli = FlaskGroup(app)

politic_urls = ['https://xml.euobserver.com/rss.xml', 'https://rss.politico.com/congress.xml', 'https://reason.com/feed/']
health_urls = ['https://rss.politico.com/healthcare.xml', 'http://rssfeeds.webmd.com/rss/rss.aspx?RSSSource=RSS_PUBLIC', 'https://www.healthphreaks.com/feed/']
sport_urls = ['http://www.sportingnews.com/us/rss', 'https://deadspin.com/rss', 'https://www.yardbarker.com/rss/rumors', 'https://www.insidesport.in/feed/']

@cli.command("load_init_db")
def load_init_db():
    for url in politic_urls:
        s = Source(url=url, category='politics')
        db.session.add(s)
        db.session.commit()
    for url in health_urls:
        s = Source(url=url, category='health')
        db.session.add(s)
        db.session.commit()
    for url in sport_urls:
        s = Source(url=url, category='sport')
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


if __name__ == "__main__":
    cli()
