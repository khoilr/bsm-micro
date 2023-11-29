import os

import pika
from dotenv import load_dotenv
from logger import logger
from rabbitmq.consumers.third_party_handler import callback as third_party_callback

# Environment variables
load_dotenv()
rabbitmq_host = os.environ.get("RABBITMQ_HOST", "103.157.218.126")
rabbitmq_port = os.environ.get("RABBITMQ_PORT", 5672)
rabbitmq_user = os.environ.get("RABBITMQ_USER", "guest")
rabbitmq_password = os.environ.get("RABBITMQ_PASSWORD", "guest")
rabbitmq_vhost = os.environ.get("RABBITMQ_VHOST", "/")
rabbitmq_is_face_presented_heartbeat_timeout = int(os.environ.get("RABBITMQ_IS_FACE_PRESENTED_HEARTBEAT_TIMEOUT", 600))

face_identification_exchange = os.environ.get("FACE_IDENTIFICATION_EXCHANGE", "face_identification")
face_identification_exchange_type = os.environ.get("FACE_IDENTIFICATION_EXCHANGE_TYPE", "fanout")
face_identification_queue = os.environ.get("FACE_IDENTIFICATION_QUEUE", "face_identification")
face_identification_heartbeat = int(os.environ.get("FACE_IDENTIFICATION_HEARTBEAT", 600))
face_identification_rpc_queue = os.environ.get("FACE_IDENTIFICATION_RPC_QUEUE", "face_identification_rpc_queue")


class RabbitMQ:
    def __init__(self) -> None:
        credentials = pika.PlainCredentials(username=rabbitmq_user, password=rabbitmq_password)
        parameters = pika.ConnectionParameters(
            host=rabbitmq_host,
            port=rabbitmq_port,
            virtual_host="/",
            credentials=credentials,
            heartbeat=rabbitmq_is_face_presented_heartbeat_timeout,
        )

        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        # Declare exchange and queue for consuming message from face_identification
        self.channel.exchange_declare(
            exchange=face_identification_exchange,
            exchange_type=face_identification_exchange_type,
            durable=True,
        )

        self.channel.queue_declare(queue=face_identification_exchange, durable=True)
        self.channel.queue_bind(exchange=face_identification_exchange, queue=face_identification_queue)

    def consume(self):
        self.channel.basic_consume(
            queue=face_identification_exchange,
            on_message_callback=third_party_callback,
            auto_ack=True,
        )
        self.channel.start_consuming()
        logger.info("[*] Waiting for messages. To exit press CTRL+C")

    def close(self):
        self.connection.close()
