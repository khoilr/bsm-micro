import os

import pika
from dotenv import load_dotenv

from src.logger import logger
from src.rabbitmq.consumers.camera_frame_capture import callback as camera_frame_capture_callback

# Environment variables
load_dotenv()
rabbitmq_host = os.environ.get("RABBITMQ_HOST", "localhost")
rabbitmq_port = os.environ.get("RABBITMQ_PORT", 5672)
rabbitmq_user = os.environ.get("RABBITMQ_USER", "guest")
rabbitmq_password = os.environ.get("RABBITMQ_PASSWORD", "guest")
rabbitmq_vhost = os.environ.get("RABBITMQ_VHOST", "/")
rabbitmq_is_face_presented_heartbeat_timeout = int(os.environ.get("RABBITMQ_IS_FACE_PRESENTED_HEARTBEAT_TIMEOUT", 600))
camera_frame_capture_exchange = os.environ.get("CAMERA_FRAME_CAPTURE_EXCHANGE", "camera_frame_capture")
camera_frame_capture_exchange_type = os.environ.get("CAMERA_FRAME_CAPTURE_EXCHANGE_TYPE", "fanout")
is_face_presented_exchange = os.environ.get("IS_FACE_PRESENTED_EXCHANGE", "is_face_presented")
is_face_presented_exchange_type = os.environ.get("IS_FACE_PRESENTED_EXCHANGE_TYPE", "fanout")
is_face_presented_queue = os.environ.get("IS_FACE_PRESENTED_QUEUE", "is_face_presented")


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

        # Declare exchange and queue for consuming message from camera_frame_capture
        self.channel.exchange_declare(
            exchange=camera_frame_capture_exchange,
            exchange_type=camera_frame_capture_exchange_type,
            durable=True,
        )
        self.camera_frame_capture_queue = self.channel.queue_declare(queue="", exclusive=True)
        self.channel.queue_bind(
            exchange=camera_frame_capture_exchange,
            queue=self.camera_frame_capture_queue.method.queue,
        )

        # Declare exchange and queue for publishing message to is_face_presented
        self.channel.exchange_declare(
            exchange=is_face_presented_exchange,
            exchange_type=is_face_presented_exchange_type,
            durable=True,
        )
        self.channel.queue_declare(queue=is_face_presented_queue, durable=True)
        self.channel.queue_bind(exchange=is_face_presented_exchange, queue=is_face_presented_queue)

    def consume(self):
        self.channel.basic_consume(
            queue=self.camera_frame_capture_queue.method.queue,
            on_message_callback=camera_frame_capture_callback,
            auto_ack=True,
        )
        self.channel.start_consuming()
        logger.info("[*] Waiting for messages. To exit press CTRL+C")

    def close(self):
        self.connection.close()
