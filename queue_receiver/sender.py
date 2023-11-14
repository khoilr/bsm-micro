import asyncio
import json
from aio_pika import connect, Message, ExchangeType
import json
import uuid


class RabbitMqProducerConfigure:
    def __init__(
        self,
        host="localhost",
        exchange="direct_logs",
        port=40000,
        user="rabbitmq",
        password="rabbitmq",
    ):
        self.host = host
        self.exchange = exchange
        self.port = port
        self.user = user
        self.password = password


class RabbitmqProducer:
    def __init__(self, config: RabbitMqProducerConfigure):
        self.config = config
        self.connection = None
        self.channel = None
        self.exchange = None
        self.futures = {}

    async def connect(self):
        self.connection = await connect(
            host=self.config.host,
            port=self.config.port,
            login=self.config.user,
            password=self.config.password,
        )

        self.channel = await self.connection.channel()
        self.callback_queue = await self.channel.declare_queue(name="reply")
        await self.callback_queue.consume(self.on_response)
        self.exchange = await self.channel.declare_exchange(
            self.config.exchange, ExchangeType.DIRECT
        )

    async def send_message(self, routing_key: str, message: str):
        correlation_id = str(uuid.uuid4())
        self.futures[correlation_id] = asyncio.Future()
        message_body = json.dumps(message).encode()
        await self.exchange.publish(
            Message(
                body=message_body,
                reply_to=self.callback_queue.name,
                correlation_id=correlation_id,
                content_type="application/json",
                delivery_mode=2,
            ),
            routing_key=routing_key,
        )

    async def on_response(self, message: Message):
        correlation_id = message.correlation_id
        payload = json.loads(message.body)
        if correlation_id in self.futures:
            payload = json.loads(message.body)
            print(payload)
            self.futures[correlation_id].set_result(message.body.decode())

    async def close_connection(self):
        await self.connection.close()


async def main():
    producer_config = RabbitMqProducerConfigure(
        host="103.157.218.126", exchange="direct_logs"
    )
    producer = RabbitmqProducer(config=producer_config)
    await producer.connect()

    # await producer.send_message(
    #     "create",
    #     json.dumps(
    #         {
    #             "person": {"name": "heo pro"},
    #             "description": "This is an item to create.",
    #         }
    #     ),
    # )
    # await producer.send_message(
    #     "update",
    #     json.dumps({"person": {"id": 23, "name": "heo vjp"}}),
    # )
    # await producer.send_message("delete", json.dumps({"person": {"id": "1"}}))
    await producer.send_message("read", json.dumps({"person": {"id": 1}}))

    await producer.close_connection()


if __name__ == "__main__":
    asyncio.run(main())
