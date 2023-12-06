import os

import pika
from dotenv import load_dotenv

from src.logger import logger
from src.services.rabbitmq.callbacks.time_keeping import callback as time_keeping_callback

load_dotenv()
rabbitmq_host = os.environ.get("RABBITMQ_HOST", "localhost")
rabbitmq_port = os.environ.get("RABBITMQ_PORT", "40000")
rabbitmq_user = os.environ.get("RABBITMQ_USER", "rabbitmq")
rabbitmq_password = os.environ.get("RABBITMQ_PASSWORD", "rabbitmq")
rabbitmq_vhost = os.environ.get("RABBITMQ_VHOST", "/")

hrm_heartbeat = int(os.environ.get("HRM_HEARTBEAT", "3600"))
hrm_queue = os.environ.get("HRM_QUEUE", "hrm_queue")

hrm_exchange = os.environ.get("HRM_EXCHANGE", "hrm_exchange")

telegram_time_keeping_queue = os.environ.get("TELEGRAM_TIME_KEEPING_QUEUE", "telegram_time_keeping_queue")


class RabbitMQ:
    def __init__(self):
        credentials = pika.PlainCredentials(username=rabbitmq_user, password=rabbitmq_password)
        parameters = pika.ConnectionParameters(
            host=rabbitmq_host,
            port=rabbitmq_port,
            virtual_host=rabbitmq_vhost,
            credentials=credentials,
            heartbeat=hrm_heartbeat,
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        # Declare queue for consuming hrm checkin
        self.channel.queue_declare(queue=hrm_queue, durable=True)

        # Declare exchange for publishing telegram notification
        self.channel.exchange_declare(exchange=hrm_exchange, exchange_type="fanout", durable=True)
        self.channel.queue_declare(queue=telegram_time_keeping_queue, durable=True)
        self.channel.queue_bind(exchange=hrm_exchange, queue=telegram_time_keeping_queue)

    def consume(self):
        logger.info(" [*] Waiting for messages. To exit press CTRL+C")
        self.channel.basic_consume(
            queue=hrm_queue,
            on_message_callback=time_keeping_callback,
            auto_ack=True,
        )
        self.channel.start_consuming()

    def close(self):
        self.connection.close()
