import datetime
import pika, sys
from parser.app import db
from parser.models import Source, Article
import json
import os
from sqlalchemy.exc import IntegrityError, PendingRollbackError

date_formats = [
    "%a, %d %b %Y %H:%M:%S",
    "%a, %d %B %Y %H:%M:%S",
    "%a %d %b %Y %H:%M:%S",
    "%d %b %Y %H:%M:%S",
]


def sport_to_json(ch, method, properties, body):
    """
    Saves today's sport articles to json format
    :param ch:
    :param method:
    :param properties:
    :param body:
    :return:
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
                break
            except ValueError:
                continue
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


def save_articles_to_db(ch, method, properties, body):
    """
    Saves health and politics articles to database
    :param ch:
    :param method:
    :param properties:
    :param body:
    :return:
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
            continue


def consumer():
    """
    Declares rabbitmq queues
    :return:
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()

    channel.queue_declare(queue="sport")
    channel.queue_declare(queue="health")
    channel.queue_declare(queue="politics")
    channel.basic_consume(
        queue="sport", on_message_callback=sport_to_json, auto_ack=True
    )
    channel.basic_consume(
        queue="health", on_message_callback=save_articles_to_db, auto_ack=True
    )
    channel.basic_consume(
        queue="politics", on_message_callback=save_articles_to_db, auto_ack=True
    )

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


def main():
    """
    Starts consuming rabbitmq messages
    :return:
    """
    try:
        consumer()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
