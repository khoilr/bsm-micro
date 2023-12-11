import json
import os

import pika
from dotenv import load_dotenv

from src.logger import logger

# Environment variables
load_dotenv()
rabbitmq_host = os.environ.get("RABBITMQ_HOST", "localhost")
rabbitmq_port = os.environ.get("RABBITMQ_PORT", 5672)
rabbitmq_user = os.environ.get("RABBITMQ_USER", "rabbitmq")
rabbitmq_password = os.environ.get("RABBITMQ_PASSWORD", "rabbitmq")
rabbitmq_vhost = os.environ.get("RABBITMQ_VHOST", "/")

registry_new_face_exchange = os.environ.get("REGISTRY_NEW_FACE_EXCHANGE", "registry.new.face.exchange")
registry_new_face_queue = os.environ.get("REGISTRY_NEW_FACE_QUEUE", "registry.new.face.queue")
registry_new_face_heartbeat = int(os.environ.get("REGISTRY_NEW_FACE_HEARTBEAT", 3600))


class RabbitMQ:
    def __init__(self):
        # Set up connection parameters
        credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
        parameters = pika.ConnectionParameters(
            host=rabbitmq_host,
            port=rabbitmq_port,
            virtual_host=rabbitmq_vhost,
            credentials=credentials,
            heartbeat=registry_new_face_heartbeat,
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        # Publishing queues
        self.channel.exchange_declare(
            exchange=registry_new_face_exchange,
            exchange_type="fanout",
            durable=True,
        )
        self.channel.queue_declare(queue=registry_new_face_queue, durable=True)
        self.channel.queue_bind(exchange=registry_new_face_exchange, queue=registry_new_face_queue)

    def close(self):
        self.connection.close()

    def publish(self, body: dict):
        self.channel.basic_publish(
            exchange=registry_new_face_exchange,
            routing_key="",
            body=json.dumps(body),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ),
        )
        logger.info(f" [x] Published to {registry_new_face_exchange} {body}")
