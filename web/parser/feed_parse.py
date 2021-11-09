import datetime

import feedparser
import asyncio
import aiohttp
import time
from parser.app import db
from parser.models import Source, Article
import json
import os


def sport_to_json():
    """
    Saves today's sport articles to json format
    :return:
    """
    date_today = datetime.date.today()
    filename = 'sport_' + date_today.strftime("%Y_%m_%d") + '.json'
    data = [article.as_dict() for article in
            Article.query.filter_by(category='sport', published_date=date_today)]
    if not os.path.exists('sport_files'):
        os.makedirs('sport_files')
    with open('sport_files/' + filename, 'w') as f:
        json.dump(data, f)


async def parse(source):
    """
    Parses news RSS feed
    :param url:
    :return:
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(source.url) as resp:
            feed = await resp.text()
    data = feedparser.parse(feed)
    for entry in data.entries:
        article = Article(url_id=source.id, category=source.category, title=entry.title, published_date=entry.published)
        db.session.add(article)
        db.session.commit()


def run_parse():
    t1 = time.time()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    source_list = Source.query.all()
    for source in source_list:
        loop.create_task(parse(source))
    tasks = asyncio.Task.all_tasks(loop=loop)
    group = asyncio.gather(*tasks, return_exceptions=True)
    loop.run_until_complete(group)
    loop.close()

    articles = Article.query.all()
    for article in articles:
        print("-" * 100)
        print("{}".format(article.title))
        print("Published at {}".format(article.published_date))
        print("-" * 100)
    sport_to_json()
    t2 = time.time()
    print(f"Spent time: {t2 - t1}")
