import os

import pika
from dotenv import load_dotenv

from logger import logger
from services.rabbitmq.callbacks.is_face_presented import callback as is_face_presented_callback
from services.rabbitmq.callbacks.rpc import callback as rpc_callback

load_dotenv()


# Environment variables
rabbitmq_host = os.environ.get("RABBITMQ_HOST", "localhost")
rabbitmq_port = os.environ.get("RABBITMQ_PORT", 5672)
rabbitmq_user = os.environ.get("RABBITMQ_USER", "rabbitmq")
rabbitmq_password = os.environ.get("RABBITMQ_PASSWORD", "rabbitmq")
rabbitmq_vhost = os.environ.get("RABBITMQ_VHOST", "/")
is_face_presented_exchange = os.environ.get("IS_FACE_PRESENTED_EXCHANGE", "is_face_presented")
is_face_presented_exchange_type = os.environ.get("IS_FACE_PRESENTED_EXCHANGE_TYPE", "fanout")
is_face_presented_queue = os.environ.get("IS_FACE_PRESENTED_QUEUE", "is_face_presented")
face_identification_exchange = os.environ.get("FACE_IDENTIFICATION_EXCHANGE", "face_identification")
face_identification_exchange_type = os.environ.get("FACE_IDENTIFICATION_EXCHANGE_TYPE", "direct")
face_identification_queue = os.environ.get("FACE_IDENTIFICATION_QUEUE", "face_identification")
face_identification_heartbeat = int(os.environ.get("FACE_IDENTIFICATION_HEARTBEAT", 600))
face_identification_rpc_queue = os.environ.get("FACE_IDENTIFICATION_RPC_QUEUE", "face_identification_rpc_queue")


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

        # Listen to exchange frames and queue frames
        self.channel.exchange_declare(
            exchange=is_face_presented_exchange,
            exchange_type=is_face_presented_exchange_type,
            durable=True,
        )
        self.channel.queue_declare(queue=is_face_presented_queue, durable=True)
        self.channel.queue_bind(exchange=is_face_presented_exchange, queue=is_face_presented_queue)

        # Declare queue for RPC
        self.channel.queue_declare(queue=face_identification_rpc_queue)

        # Declare queue for publishing face identification
        self.channel.exchange_declare(
            exchange=face_identification_exchange,
            exchange_type=face_identification_exchange_type,
            durable=True,
        )
        self.channel.queue_declare(queue=face_identification_queue, durable=True)
        self.channel.queue_bind(exchange=face_identification_exchange, queue=face_identification_queue)

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
