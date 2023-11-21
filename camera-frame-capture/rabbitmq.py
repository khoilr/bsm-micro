import os

import pika
from dotenv import load_dotenv

from logger import logger

# Environment variables
load_dotenv()
rabbitmq_host = os.environ.get("RABBITMQ_HOST", "localhost")
rabbitmq_port = os.environ.get("RABBITMQ_PORT", 5672)
rabbitmq_user = os.environ.get("RABBITMQ_USER", "guest")
rabbitmq_password = os.environ.get("RABBITMQ_PASSWORD", "guest")
rabbitmq_vhost = os.environ.get("RABBITMQ_VHOST", "/")
camera_frame_capture_exchange = os.environ.get("CAMERA_FRAME_CAPTURE_EXCHANGE", "camera_frame_capture")
camera_frame_capture_exchange_type = os.environ.get("CAMERA_FRAME_CAPTURE_EXCHANGE_TYPE", "fanout")
camera_frame_capture_queue = os.environ.get("CAMERA_FRAME_CAPTURE_QUEUE", "camera_frame_capture")
camera_frame_capture_heartbeat = int(os.environ.get("CAMERA_FRAME_CAPTURE_HEARTBEAT", 600))
camera_frame_capture_camera_url = os.environ.get("CAMERA_FRAME_CAPTURE_CAMERA_URL")
camera_frame_capture_camera_name = os.environ.get("CAMERA_FRAME_CAPTURE_CAMERA_NAME")


class RabbitMQ:
    def __init__(self) -> None:
        credentials = pika.PlainCredentials(username=rabbitmq_user, password=rabbitmq_password)
        parameters = pika.ConnectionParameters(
            host=rabbitmq_host,
            port=rabbitmq_port,
            virtual_host=rabbitmq_vhost,
            credentials=credentials,
            heartbeat=camera_frame_capture_heartbeat,
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        # create a queue and topic exchange and bind them together
        self.channel.exchange_declare(
            exchange=camera_frame_capture_exchange,
            exchange_type=camera_frame_capture_exchange_type,
            durable=True,
        )
        self.channel.queue_declare(
            queue=camera_frame_capture_queue,
            durable=True,
        )
        self.channel.queue_bind(
            exchange=camera_frame_capture_exchange,
            queue=camera_frame_capture_queue,
        )

    def send(self, message: str):
        self.channel.basic_publish(
            exchange=camera_frame_capture_exchange,
            routing_key=camera_frame_capture_queue,
            body=message,
            properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE),
        )
        logger.info(f" [x] Sent {message[:100]}")

    def close(self):
        self.connection.close()
