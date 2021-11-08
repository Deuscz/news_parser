import feedparser
import asyncio
import aiohttp
from collections import namedtuple
import time

Feed = namedtuple("Feed", ["title", "link", "publish_date"])

urls = [
    "http://feeds.bbci.co.uk/news/world/rss.xml",
    "https://www.nytimes.com/svc/collections/v1/publish/https://www.nytimes.com/section/world/rss.xml",
    "https://www.aljazeera.com/xml/rss/all.xml",
]


# urls = ['https://xml.euobserver.com/rss.xml']


async def parse(url):
    """
    Parses news RSS feed
    :param url:
    :return:
    """
    news_list = []
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            feed = await resp.text()
    data = feedparser.parse(feed)
    for entry in data.entries:
        news_list.append(
            Feed(title=entry.title, link=entry.link, publish_date=entry.published)
        )
    return news_list


if __name__ == "__main__":
    t1 = time.time()
    loop = asyncio.get_event_loop()
    for url in urls:
        loop.create_task(parse(url))
    tasks = asyncio.Task.all_tasks(loop=loop)
    group = asyncio.gather(*tasks, return_exceptions=True)
    loop.run_until_complete(group)
    loop.close()
    t2 = time.time()
    for task_result in group.result():
        for feed in task_result:
            print("-" * 100)
            print("{}[{}]".format(feed.title, feed.link))
            print("Published at {}".format(feed.publish_date))
            print("-" * 100)
    print(f"Spent time: {t2 - t1}")
