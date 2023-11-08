import asyncio
import json
from aio_pika import connect, Message, ExchangeType
import json 

class RabbitMqProducerConfigure:
    def __init__(self, host='localhost', exchange='direct_logs', port=5672, user='rabbitmq', password='rabbitmq'):
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

    async def connect(self):
        self.connection = await connect(
            host=self.config.host,
            port=self.config.port,
            login=self.config.user,
            password=self.config.password
        )

        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange(self.config.exchange, ExchangeType.DIRECT)

    async def send_message(self, routing_key, message):
        message_body = json.dumps(message).encode()
        await self.exchange.publish(
            Message(
                body=message_body,
                content_type='application/json',
                delivery_mode=2
            ),
            routing_key=routing_key
        )
        print(f"Sent {routing_key} message: {message}")

    async def close_connection(self):
        await self.connection.close()

async def main():
    producer_config = RabbitMqProducerConfigure(host='103.157.218.126', exchange='direct_logs')
    producer = RabbitmqProducer(config=producer_config)
    await producer.connect()

    await producer.send_message('create', json.dumps({'item': 'Item 1', 'description': 'This is an item to create.'}))
    await producer.send_message('read', json.dumps({'item_id': '12345'}))
    await producer.send_message('update', json.dumps({'item_id': '12345', 'description': 'Updated description.'}))
    await producer.send_message('delete', json.dumps({'item_id': '12345'}))

    await producer.close_connection()

if __name__ == '__main__':
    asyncio.run(main())
