import datetime
import json
import os
import sys
from multiprocessing import Process
from parser.app import db
from parser.models import Article, Source

import pika
from sqlalchemy.exc import IntegrityError, PendingRollbackError

date_formats = [
    "%a, %d %b %Y %H:%M:%S",
    "%a, %d %B %Y %H:%M:%S",
    "%a %d %b %Y %H:%M:%S",
    "%d %b %Y %H:%M:%S",
]


def sport_to_json(ch, method, properties, body: str) -> None:
    """
    Saves today's sport articles to json format.
    """
    date_today = datetime.date.today()
    filename = "sport_" + date_today.strftime("%Y-%m-%d") + ".txt"
    articles = json.loads(body)
    data = []
    for article in articles:
        for date_format in date_formats:
            try:
                published_date = datetime.datetime.strptime(
                    " ".join(article[3].split(" ")[:-1]), date_format
                ).date()
            except ValueError:
                pass
        if published_date == date_today:
            data.append(
                {
                    "url_id": article[0],
                    "category": article[1],
                    "title": article[2],
                    "published_date": published_date.strftime("%Y-%m-%d"),
                }
            )
    if not os.path.exists("sport_files"):
        os.makedirs("sport_files")
    with open("sport_files/" + filename, "w") as f:
        json.dump(data, f)


def save_articles_to_db(ch, method, properties, body: str) -> None:
    """
    Saves health and politics articles to database.
    """
    articles = json.loads(body)
    for article in articles:
        try:
            db.session.add(
                Article(
                    url_id=article[0],
                    category=article[1],
                    title=article[2],
                    published_date=article[3],
                )
            )
            db.session.commit()
        except (IntegrityError, PendingRollbackError):
            db.session.rollback()
            continue


class ConsumerFactory:
    """
    Class-factory for consumer definition.
    """

    def __init__(self, queue="sport", callback=sport_to_json, b="b1", e="e1"):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="rabbitmq")
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=e, durable="true")
        result = self.channel.queue_declare(queue=queue, durable="false")
        queue_name = result.method.queue
        binding_key = b
        self.channel.queue_bind(exchange=e, queue=queue_name, routing_key=binding_key)
        self.channel.basic_consume(
            queue=queue, on_message_callback=callback, auto_ack=True
        )

    def run(self):
        self.channel.start_consuming()


def main() -> None:
    """
    Starts consuming rabbitmq messages
    """
    try:
        subscriber_list = []
        subscriber_list.append(
            ConsumerFactory(queue="sport", callback=sport_to_json, b="b1", e="e1")
        )
        subscriber_list.append(
            ConsumerFactory(
                queue="health", callback=save_articles_to_db, b="b2", e="e2"
            )
        )
        subscriber_list.append(
            ConsumerFactory(
                queue="politics", callback=save_articles_to_db, b="b3", e="e3"
            )
        )

        process_list = []
        for sub in subscriber_list:
            process = Process(target=sub.run)
            process.start()
            process_list.append(process)

        for process in process_list:
            process.join()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
