import asyncio
import json
from aio_pika import connect, ExchangeType, Message
from loguru import logger
import json
from database.dao import FaceDAO, PersonDAO
from database.db_config import init_db


class MetaClass(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class RabbitMqServerConfigure(metaclass=MetaClass):
    def __init__(
        self,
        host: str = "103.157.218.126",
        queue: str = "task",
        exchange: str = "direct_logs",
        port: int = 40000,
        user: str = "rabbitmq",
        password: str = "rabbitmq",
    ):
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

    async def connect(self):
        self.connection = await connect(
            host=self.server.host,
            port=self.server.port,
            login=self.server.user,
            password=self.server.password,
        )

        self.channel = await self.connection.channel()
        exchange = await self.channel.declare_exchange(
            self.server.exchange, ExchangeType.DIRECT
        )

        for operation in ["create", "read", "update", "delete"]:
            queue_name = f"{self.server.queue}_{operation}"
            queue = await self.channel.declare_queue(queue_name)
            await queue.bind(exchange, routing_key=operation)

        logger.info("Server started waiting for Messages")

    async def consume(self):
        for operation in ["create", "read", "update", "delete"]:
            queue_name = f"{self.server.queue}_{operation}"
            queue = await self.channel.get_queue(queue_name)
            await queue.consume(self.on_message)

    async def on_message(self, message: Message):
        async with message.process():
            payload = json.loads(message.body)
            operation = message.routing_key
            response = await getattr(self, operation)(payload)
            print(response)
            if message.reply_to:
                await self.channel.default_exchange.publish(
                    Message(
                        body=json.dumps(response).encode(),
                        correlation_id=message.correlation_id,
                    ),
                    routing_key=message.reply_to,
                )

    async def create(self, payload):
        logger.info(f"Creating: {payload}")
        data: dict = json.loads(payload)
        face_data = data.get("face", None)
        person_data = data.get("person", None)

        if face_data:
            FaceDAO.create_face(
                frame_file_path=person_data["path"],
                x=person_data["x"],
                y=person_data["y"],
                width=person_data["width"],
                height=person_data["height"],
            )

        if person_data:
            person_object = PersonDAO.create_person(person_data["name"])
            logger.info(person_object)

    async def read(self, payload):
        logger.info(f"Reading: {payload}")
        data: dict = json.loads(payload)
        face_data = data.get("face", None)
        person_data = data.get("person", None)

        if face_data:
            face_data = FaceDAO.get_face_by_id(face_id=face_data["id"]).to_json()

        if person_data:
            person_data = PersonDAO.get_person_by_id(person_id=person_data["id"])
            person_data = person_data.to_json()

        return_data = (face_data, person_data)
        
        return return_data

    async def update(self, payload):
        logger.info(f"Updating: {payload}")
        data: dict = json.loads(payload)
        logger.info(data)
        face_data = data.get("face", None)
        person_data = data.get("person", None)

        if face_data:
            face_id = face_data.pop("id")
            FaceDAO.update_face(face_id=face_id, **face_data)

        if person_data:
            person_id = person_data.pop("id")
            PersonDAO.update_person(person_id=person_id, **person_data)

    async def delete(self, payload):
        logger.info(f"Deleting: {payload}")
        data: dict = json.loads(payload)
        face_data = data.get("face", None)
        person_data = data.get("person", None)

        if face_data:
            FaceDAO.delete_face(face_id=face_data["id"])

        if person_data:
            PersonDAO.delete_person(person_id=person_data["id"])

    async def start_server(self):
        await self.connect()
        await self.consume()


def main():
    init_db()
    server_config = RabbitMqServerConfigure()
    server = RabbitmqServer(server=server_config)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(server.start_server())
    loop.run_forever()


if __name__ == "__main__":
    main()
