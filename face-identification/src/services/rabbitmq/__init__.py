import os

import pika
from dotenv import load_dotenv

from src.logger import logger
from src.services.rabbitmq.callbacks.is_face_presented import callback as is_face_presented_callback
from src.services.rabbitmq.callbacks.rpc import callback as rpc_callback

load_dotenv()


# Environment variables
rabbitmq_host = os.environ.get("RABBITMQ_HOST", "localhost")
rabbitmq_port = os.environ.get("RABBITMQ_PORT", 5672)
rabbitmq_user = os.environ.get("RABBITMQ_USER", "rabbitmq")
rabbitmq_password = os.environ.get("RABBITMQ_PASSWORD", "rabbitmq")
rabbitmq_vhost = os.environ.get("RABBITMQ_VHOST", "/")

is_face_presented_queue = os.environ.get("IS_FACE_PRESENTED_QUEUE", "is_face_presented")

face_identification_exchange = os.environ.get("FACE_IDENTIFICATION_EXCHANGE", "face_identification")
face_identification_heartbeat = int(os.environ.get("FACE_IDENTIFICATION_HEARTBEAT", 600))

face_identification_rpc_queue = os.environ.get("FACE_IDENTIFICATION_RPC_QUEUE", "face_identification_rpc_queue")

hrm_queue = os.environ.get("HRM_QUEUE", "hrm_queue")
telegram_unknown_queue = os.environ.get("TELEGRAM_UNKNOWN_QUEUE", "telegram_unknown_queue")


class RabbitMQ:
    def __init__(self):
        # Set up connection parameters
        credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
        parameters = pika.ConnectionParameters(
            host=rabbitmq_host,
            port=rabbitmq_port,
            virtual_host=rabbitmq_vhost,
            credentials=credentials,
            heartbeat=face_identification_heartbeat,
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        # Consuming queues
        self.channel.queue_declare(queue=is_face_presented_queue, durable=True)
        self.channel.queue_declare(queue=face_identification_rpc_queue)

        # Publishing queues
        self.channel.exchange_declare(
            exchange=face_identification_exchange,
            exchange_type="direct",
            durable=True,
        )
        self.channel.queue_declare(queue=hrm_queue, durable=True)
        self.channel.queue_declare(queue=telegram_unknown_queue, durable=True)
        self.channel.queue_bind(exchange=face_identification_exchange, queue=hrm_queue)
        self.channel.queue_bind(exchange=face_identification_exchange, queue=telegram_unknown_queue)

    def consume(self):
        self.channel.basic_consume(
            queue=is_face_presented_queue,
            on_message_callback=is_face_presented_callback,
            auto_ack=True,
        )
        self.channel.basic_consume(
            queue=face_identification_rpc_queue,
            on_message_callback=rpc_callback,
        )

        logger.info("[*] Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()

    def close(self):
        self.connection.close()
