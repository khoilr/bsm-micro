import os
import time
import uuid

import pika
from dotenv import load_dotenv

# Environment variables
load_dotenv()
rabbitmq_host = os.environ.get("RABBITMQ_HOST", "localhost")
rabbitmq_port = os.environ.get("RABBITMQ_PORT", 40000)
rabbitmq_user = os.environ.get("RABBITMQ_USER", "rabbitmq")
rabbitmq_password = os.environ.get("RABBITMQ_PASSWORD", "rabbitmq")
rabbitmq_vhost = os.environ.get("RABBITMQ_VHOST", "/")
gateway_api_heartbeat = int(os.environ.get("GATEWAY_API_HEARTBEAT", 300))
face_identification_rpc_queue = os.environ.get("FACE_IDENTIFICATION_RPC", "face_identification_rpc_queue")


class CameraRPCClient:
    def __init__(self):
        credential = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
        parameters = pika.ConnectionParameters(
            host=rabbitmq_host,
            port=rabbitmq_port,
            virtual_host=rabbitmq_vhost,
            credentials=credential,
            heartbeat=gateway_api_heartbeat,
        )
        self.connection = pika.BlockingConnection(parameters=parameters)
        self.channel = self.connection.channel()

        result = self.channel.queue_declare("", exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True,
        )

    def on_response(self, ch, method, props, body):  # pylint: disable=unused-argument
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, body):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange="",
            routing_key=face_identification_rpc_queue,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=body,
        )

        start_time = time.time()
        while self.response is None:
            self.connection.process_data_events()
            if time.time() - start_time > 20:  # Timeout after 10 seconds
                raise TimeoutError("RPC call timed out")

        return self.response
