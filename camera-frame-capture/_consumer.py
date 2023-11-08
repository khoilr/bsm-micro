"""Consumer example"""

import json
import pika

# Connect to RabbitMQ
credentials = pika.PlainCredentials("rabbitmq", "rabbitmq")
connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", credentials=credentials))
channel = connection.channel()

# Declare the exchange and bind the queue
channel.exchange_declare(exchange="frames", exchange_type="fanout")
result = channel.queue_declare(queue="", exclusive=True)
channel.queue_bind(exchange="frames", queue=result.method.queue)


# Callback function
def callback(ch, method, properties, body):
    frame = json.loads(body)
    print(frame)


# Start consuming
channel.basic_consume(queue=result.method.queue, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
