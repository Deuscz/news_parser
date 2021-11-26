import datetime
import json
import os
from multiprocessing import Process
from parser.config import db
from parser.models import Article
from parser.utils import get_articles_data_from_feed
from typing import Any, Callable, Dict, List, Tuple, Union

import pika


def sport_to_json(*args) -> None:
    """Save today's sport articles to file in json format.

    Args:
        args: list of arguments:
            args[0]: channel
            args[1]: method
            args[2]: properties
            args[3]: message body
    """
    filename = "sport_" + datetime.date.today().strftime("%Y-%m-%d") + ".txt"
    articles = json.loads(args[3])
    data = get_articles_data_from_feed(articles)
    if not os.path.exists("sport_files"):
        os.makedirs("sport_files")
    with open("sport_files/" + filename, "w", encoding='utf8') as f:
        json.dump(data, f)


def save_articles_to_db(*args) -> None:
    """Save health and politics articles to database.

    Args:
        args: list of arguments:
            args[0]: channel
            args[1]: method
            args[2]: properties
            args[3]: message body
    """
    articles = json.loads(args[3])
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


class ConsumerFactory:
    """Class-factory for consumer definition.

    Args:
        queue: name of queue to consume
        callback: callback function
        b: binding key
        e: exchange
    """

    def __init__(self, queue: str = "sport", callback: Callable[
        [pika.channel.Channel, pika.spec.Basic.Return, pika.spec.BasicProperties, bytes], None] = sport_to_json,
                 b: str = "b1",
                 e: str = "e1") -> None:
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="rabbitmq")
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=e, durable="true")
        result = self.channel.queue_declare(queue=queue, durable="true")
        queue_name = result.method.queue
        binding_key = b
        self.channel.queue_bind(exchange=e, queue=queue_name, routing_key=binding_key)
        self.channel.basic_consume(
            queue=queue, on_message_callback=callback, auto_ack=True
        )

    def run(self) -> None:
        """Start queue consuming."""
        self.channel.start_consuming()


# Dict with queues and callback functions
CALLBACKS: Dict[str, Union[Callable[[Tuple[Any, ...]], None], Callable[[Tuple[Any, ...]], None]]] = {
    'sport': sport_to_json,
    'health': save_articles_to_db,
    'politics': save_articles_to_db,
}


def get_subscriber_list() -> List[ConsumerFactory]:
    """Return subscribers list.

    Returns:
        list of queues subscribers
    """
    subscriber_list = []
    for i, queue in enumerate(CALLBACKS):
        subscriber_list.append(
            ConsumerFactory(queue=queue, callback=CALLBACKS[queue], b="b" + str(i), e="e" + str(i))
        )
    return subscriber_list


def main() -> None:
    """Start consuming rabbitmq messages."""

    subscriber_list = get_subscriber_list()
    process_list = []
    for sub in subscriber_list:
        process = Process(target=sub.run)
        process.start()
        process_list.append(process)

    for process in process_list:
        process.join()
