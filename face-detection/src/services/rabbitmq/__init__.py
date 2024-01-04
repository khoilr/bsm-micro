import asyncio
import os

import aio_pika
from dotenv import load_dotenv

from src.logger import logger
from src.services.rabbitmq.callbacks.capture_frame import handler as frame_capture_callback

# Load environment variables
load_dotenv()
rabbitmq_host = os.environ.get("RABBITMQ_HOST", "localhost")
rabbitmq_port = int(os.environ.get("RABBITMQ_PORT", 40000))
rabbitmq_user = os.environ.get("RABBITMQ_USER", "khoilr")
rabbitmq_password = os.environ.get("RABBITMQ_PASSWORD", "khoilr")
rabbitmq_vhost = os.environ.get("RABBITMQ_VHOST", "bsm")


class FaceDetectionService:
    def __init__(self) -> None:
        self.connection: aio_pika.Connection = None
        self.channel: aio_pika.Channel = None
        self.face_detection_exchange: aio_pika.Exchange = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(
            host=rabbitmq_host,
            port=rabbitmq_port,
            login=rabbitmq_user,
            password=rabbitmq_password,
            virtualhost=rabbitmq_vhost,
        )
        self.channel = await self.connection.channel()
        logger.info("Connected to RabbitMQ")

    async def declare_exchange(self):
        # Declare exchange and queue for publishing message to is_face_presented
        self.face_detection_exchange = await self.channel.declare_exchange(
            name="face.detection",
            type=aio_pika.ExchangeType.FANOUT,
            durable=True,
        )
        queue = await self.channel.declare_queue(
            name="face.recognition",
            durable=True,
        )
        await queue.bind(self.face_detection_exchange)

    async def publish(self, message: aio_pika.Message):
        await self.face_detection_exchange.publish(
            message=message,
            routing_key="",
        )

    async def consume_exchange(
        self,
        handler: callable,
        exchange_name: str,
        exchange_type: aio_pika.ExchangeType = aio_pika.ExchangeType.FANOUT,
        durable: bool = True,
    ):
        exchange = await self.channel.declare_exchange(
            name=exchange_name,
            type=exchange_type,
            durable=durable,
        )
        queue = await self.channel.declare_queue(exclusive=True)
        await queue.bind(exchange)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                await handler(message, self.face_detection_exchange)

    async def start_consuming(self):
        logger.info("Start consuming message from capture.frame")
        tasks = [
            asyncio.create_task(
                self.consume_exchange(
                    handler=frame_capture_callback,
                    exchange_name="capture.frame",
                    exchange_type=aio_pika.ExchangeType.FANOUT,
                    durable=True,
                )
            )
        ]
        await asyncio.gather(*tasks)

    async def close(self):
        await self.connection.close()
