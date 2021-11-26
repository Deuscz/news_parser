import asyncio
import json
from parser.models import Source
from typing import List, Tuple, Union

import aiohttp
import feedparser
import pika


async def parse(source: Source) -> Tuple[str, List[list]]:
    """Parse news RSS feed.

    Args:
        source: news source model
    Returns:
        source category and list of articles
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(source.url) as resp:
            feed = await resp.text()
    data = feedparser.parse(feed)
    result_list = []
    for entry in data.entries:
        article = [source.id, source.category, entry.title, entry.published]
        result_list.append(article)
    return source.category, result_list


def run_async_loop() -> Union:
    """Create asyncio loop and start parsing

    Returns:
        group of completed tasks
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    source_list = Source.query.all()
    for source in source_list:
        loop.create_task(parse(source))
    tasks = asyncio.Task.all_tasks(loop=loop)
    group = asyncio.gather(*tasks, return_exceptions=True)
    loop.run_until_complete(group)
    loop.close()
    return group


def run_parse() -> None:
    """Start RSS feed parsing and sends messages to rabbitmq queues."""
    group = run_async_loop()
    sport_list = []
    health_list = []
    politics_list = []
    for category, article_list in group.result():
        if category == "sport":
            sport_list += article_list
        elif category == "health":
            health_list += article_list
        elif category == "politics":
            politics_list += article_list
    send_mq("sport", json.dumps(sport_list))
    send_mq("health", json.dumps(health_list))
    send_mq("politics", json.dumps(politics_list))


def send_mq(queue: str, message: str) -> None:
    """Establish connection to rabbitmq queue and sends message.

    Args:
        queue: name of queue
        message: message to send
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()

    channel.queue_declare(queue=queue, durable="false")

    channel.basic_publish(exchange="", routing_key=queue, body=message)
    connection.close()
