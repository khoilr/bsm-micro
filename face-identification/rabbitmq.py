import os

import pika
from dotenv import load_dotenv

from logger import logger

load_dotenv()


# Environment variables
rabbitmq_host = os.environ.get("RABBITMQ_HOST", "localhost")
rabbitmq_port = os.environ.get("RABBITMQ_PORT", 5672)
rabbitmq_username = os.environ.get("RABBITMQ_USERNAME", "rabbitmq")
rabbitmq_password = os.environ.get("RABBITMQ_PASSWORD", "rabbitmq")
rabbitmq_vhost = os.environ.get("RABBITMQ_VHOST", "/")
rabbitmq_exchange = os.environ.get("RABBITMQ_EXCHANGE", "frames")


class RabbitMQ:
    def __init__(
        self,
        host=rabbitmq_host,
        port=rabbitmq_port,
        username=rabbitmq_username,
        password=rabbitmq_password,
        vhost=rabbitmq_vhost,
        exchange=rabbitmq_exchange,
    ):
        # Set up connection parameters
        credentials = pika.PlainCredentials(username, password)
        parameters = pika.ConnectionParameters(
            host=host,
            port=port,
            virtual_host=vhost,
            credentials=credentials,
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        # Declare exchange and queue
        self.channel.exchange_declare(exchange=exchange, exchange_type="fanout")
        self.queue = self.channel.queue_declare(queue="", exclusive=True)
        self.queue_name = self.queue.method.queue
        self.channel.queue_bind(exchange=rabbitmq_exchange, queue=self.queue_name)

    def consume(self, on_message_callback):
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=on_message_callback,
            auto_ack=True,
        )
        logger.info("[*] Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()

    def close(self):
        self.connection.close()
