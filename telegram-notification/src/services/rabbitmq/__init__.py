import os

import pika
from dotenv import load_dotenv

from src.logger import logger
from src.services.rabbitmq.callbacks.time_keeping import callback as time_keeping_callback
from src.services.rabbitmq.callbacks.unknown import callback as unknown_callback

# Environment variables
load_dotenv()
rabbitmq_host = os.environ.get("RABBITMQ_HOST", "103.157.218.126")
rabbitmq_port = os.environ.get("RABBITMQ_PORT", 5672)
rabbitmq_user = os.environ.get("RABBITMQ_USER", "guest")
rabbitmq_password = os.environ.get("RABBITMQ_PASSWORD", "guest")
rabbitmq_vhost = os.environ.get("RABBITMQ_VHOST", "/")

telegram_notification_heartbeat = int(os.environ.get("TELEGRAM_NOTIFICATION_HEARTBEAT", 600))
telegram_unknown_queue = os.environ.get("TELEGRAM_UNKNOWN_QUEUE", "telegram_unknown_queue")
telegram_time_keeping_queue = os.environ.get("TELEGRAM_TIME_KEEPING_QUEUE", "telegram_time_keeping_queue")


class RabbitMQ:
    def __init__(self) -> None:
        credentials = pika.PlainCredentials(username=rabbitmq_user, password=rabbitmq_password)
        parameters = pika.ConnectionParameters(
            host=rabbitmq_host,
            port=rabbitmq_port,
            virtual_host="/",
            credentials=credentials,
            heartbeat=telegram_notification_heartbeat,
        )

        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=telegram_unknown_queue, durable=True)
        self.channel.queue_declare(queue=telegram_time_keeping_queue, durable=True)

    def consume(self):
        logger.info("[*] Waiting for messages. To exit press CTRL+C")
        self.channel.basic_consume(
            queue=telegram_unknown_queue,
            on_message_callback=unknown_callback,
            auto_ack=True,
        )
        self.channel.basic_consume(
            queue=telegram_time_keeping_queue,
            on_message_callback=time_keeping_callback,
            auto_ack=True,
        )
        self.channel.start_consuming()

    def close(self):
        self.connection.close()
