import asyncio
import json
from aio_pika import connect, ExchangeType
from loguru import logger
import json
from database.dao import FaceDAO, PersonDAO
from database.db_config import init_db, Session
class MetaClass(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class RabbitMqServerConfigure(metaclass=MetaClass):
    def __init__(self, host='localhost', queue='hello', exchange='direct_logs', port=5672, user='rabbitmq', password='rabbitmq'):
        self.host = host
        self.queue = queue
        self.exchange = exchange
        self.port = port
        self.user = user
        self.password = password

class RabbitmqServer:
    def __init__(self, server: RabbitMqServerConfigure):
        self.server = server
        self.connection = None
        self.channel = None
        init_db()

    async def connect(self):
        self.connection = await connect(
            host=self.server.host,
            port=self.server.port,
            login=self.server.user,
            password=self.server.password
        )

        self.channel = await self.connection.channel()
        exchange = await self.channel.declare_exchange(self.server.exchange, ExchangeType.DIRECT)

        for operation in ['create', 'read', 'update', 'delete']:
            queue_name = f"{self.server.queue}_{operation}"
            queue = await self.channel.declare_queue(queue_name)
            await queue.bind(exchange, routing_key=operation)

        logger.info("Server started waiting for Messages")

    async def consume(self):
        for operation in ['create', 'read', 'update', 'delete']:
            queue_name = f"{self.server.queue}_{operation}"
            queue = await self.channel.get_queue(queue_name)
            await queue.consume(self.on_message)

    async def on_message(self, message):
        async with message.process():
            payload = json.loads(message.body)
            operation = message.routing_key
            logger.info(f"Received {operation} request: {payload}")
            await getattr(self, operation)(payload)

    async def create(self, payload):
        logger.info(f"Creating: {payload}")
        data = json.loads(payload)
        face_data = data.get("face", None)
        person_data = data.get("person", None)

        if face_data:
            pass

        if person_data:
            pass

        

    async def read(self, payload):
        logger.info(f"Reading: {payload}")
        data = json.loads(payload)
        face_data = data.get("face", None)
        person_data = data.get("person", None)

        if face_data:
            pass

        if person_data:
            pass

    async def update(self, payload):
        logger.info(f"Updating: {payload}")
        data = json.loads(payload)
        face_data = data.get("face", None)
        person_data = data.get("person", None)

        if face_data:
            pass

        if person_data:
            pass

    async def delete(self, payload):
        logger.info(f"Deleting: {payload}")
        data = json.loads(payload)
        face_data = data.get("face", None)
        person_data = data.get("person", None)

        if face_data:
            pass

        if person_data:
            pass
        
    async def start_server(self):
        await self.connect()
        await self.consume()

if __name__ == "__main__":
    server_config = RabbitMqServerConfigure(host='103.157.218.126', queue='task')
    server = RabbitmqServer(server=server_config)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(server.start_server())
    loop.run_forever()
