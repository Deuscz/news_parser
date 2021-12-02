import asyncio
import datetime
import json
import os
from parser.config import db
from parser.models import Article
from parser.utils import get_articles_data_from_feed
from typing import Any, Callable, Coroutine, Dict

import aio_pika


def process_message(consumer) -> Callable[[aio_pika.IncomingMessage], Coroutine[Any, Any, Callable[[str], None]]]:
    """RabbitMQ message processor.

    Args:
        consumer: consumer callback function
    Returns:
        wrapped function
    """

    async def wrapper(message: aio_pika.IncomingMessage) -> Callable[[str], None]:
        """Async wrapper for consumer callback function.

        Args:
            message: aio-pika message
        Returns:
            awaited consumer callback function
        """
        async with message.process():
            return await consumer(message.body.decode())

    return wrapper


@process_message
async def sport_to_json(message: str) -> None:
    """Save today's sport articles to file in json format.

    Args:
        message: rabbitmq message body
    """
    filename = "sport_" + datetime.date.today().strftime("%Y-%m-%d") + ".txt"
    articles = json.loads(message)
    data = get_articles_data_from_feed(articles)
    if not os.path.exists("sport_files"):
        os.makedirs("sport_files")
    with open("sport_files/" + filename, "w", encoding='utf8') as f:
        json.dump(data, f)


@process_message
async def save_articles_to_db(message: str) -> None:
    """Save health and politics articles to database.

    Args:
        message: rabbitmq message body
    """
    articles = json.loads(message)
    articles = [article for article in articles if
                Article.query.filter_by(title=article[2]).first() is None and article[3] and article[2]]
    if articles:
        articles_to_commit = [Article(url_id=article[0],  # article[0]: uld_id
                                      category=article[1],  # article[1]: category
                                      title=article[2],  # article[2]: title
                                      published_date=article[3],  # article[3]: published_date
                                      ) for article in articles]
        db.session.add_all(articles_to_commit)
        db.session.commit()


# Dict with queues and callback functions
CALLBACKS: Dict[str, Callable[[Any], Coroutine[Any, Any, Callable[[str], None]]]] = {
    'sport': sport_to_json,
    'health': save_articles_to_db,
    'politics': save_articles_to_db,
}


async def main(loop: asyncio.AbstractEventLoop) -> aio_pika.connection.Connection:
    """Establish rabbitmq connection and start consuming.

    Args:
        loop: asyncio loop
    Returns:
        aio-pika connection
    """
    connection = await aio_pika.connect_robust(
        host="rabbitmq", loop=loop
    )

    # Creating channel
    channel = await connection.channel()
    queues = {}
    # Declaring queue
    for queue in list(CALLBACKS.keys()):
        queues[queue] = await channel.declare_queue(queue, auto_delete=True)
    # Run consumers
    for queue_name, queue in queues.items():
        await queue.consume(CALLBACKS[queue_name])

    return connection


def run_consumers():
    """Run main consumer asyncio loop."""
    loop = asyncio.get_event_loop()
    connection = loop.run_until_complete(main(loop))

    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(connection.close())
