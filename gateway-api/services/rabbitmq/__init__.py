import os
import uuid

import pika
from dotenv import load_dotenv

load_dotenv()

BSM_SERVER_RABBITMQ_HOST = os.environ.get("BSM_SERVER_RABBITMQ_HOST", "localhost")
BSM_SERVER_RABBITMQ_PORT = os.environ.get("BSM_SERVER_RABBITMQ_PORT", 4000)
BSM_SERVER_RABBITMQ_USER = os.environ.get("BSM_SERVER_RABBITMQ_USER", "rabbitmq")
BSM_SERVER_RABBITMQ_PASS = os.environ.get("BSM_SERVER_RABBITMQ_PASS", "rabbitmq")
BSM_SERVER_RABBITMQ_VHOST = os.environ.get("BSM_SERVER_RABBITMQ_VHOST", "/")
BSM_SERVER_RABBITMQ_HEARTBEAT_TIMEOUT = int(os.environ.get("BSM_SERVER_RABBITMQ_HEARTBEAT_TIMEOUT", 600))
BSM_SERVER_ROUTING_KEY = os.environ.get("BSM_SERVER_ROUTING_KEY", "rpc_queue")


class CameraRPCClient:
    def __init__(self):
        credentials = pika.PlainCredentials(
            username=BSM_SERVER_RABBITMQ_USER,
            password=BSM_SERVER_RABBITMQ_PASS,
        )
        parameters = pika.ConnectionParameters(
            host=BSM_SERVER_RABBITMQ_HOST,
            port=BSM_SERVER_RABBITMQ_PORT,
            credentials=credentials,
            heartbeat=BSM_SERVER_RABBITMQ_HEARTBEAT_TIMEOUT,
        )
        self.connection = pika.BlockingConnection(parameters=parameters)
        self.channel = self.connection.channel()

        queue = self.channel.queue_declare(queue="", exclusive=True)
        self.callback_queue = queue.method.queue

        self.channel.basic_consume(queue=self.callback_queue, on_message_callback=self.on_response, auto_ack=True)

        self.response = None

    def on_response(self, ch, method, props, body):  # pylint: disable=unused-argument
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange="",
            routing_key=BSM_SERVER_ROUTING_KEY,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=n,
        )

        while self.response is None:
            self.connection.process_data_events()
        return self.response
