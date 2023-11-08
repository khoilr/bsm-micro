import json
import os
from datetime import datetime
import redis
import cv2
import numpy as np
import pika
import pytz
from dotenv import load_dotenv

from processors.recognize import recognize

load_dotenv()

# Environment variables
rabbitmq_host = os.environ.get("RABBITMQ_HOST", "localhost")
rabbitmq_port = os.environ.get("RABBITMQ_PORT", 5672)
rabbitmq_username = os.environ.get("RABBITMQ_USERNAME", "rabbitmq")
rabbitmq_password = os.environ.get("RABBITMQ_PASSWORD", "rabbitmq")
rabbitmq_vhost = os.environ.get("RABBITMQ_VHOST", "/")
rabbitmq_exchange = os.environ.get("RABBITMQ_EXCHANGE", "camera_frame_capture")

# Set up connection parameters
credentials = pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
parameters = pika.ConnectionParameters(
    host=rabbitmq_host,
    port=rabbitmq_port,
    virtual_host=rabbitmq_vhost,
    credentials=credentials,
)

# Create connection and channel
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Declare exchange and queue
channel.exchange_declare(exchange=rabbitmq_exchange, exchange_type="fanout")
result = channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange=rabbitmq_exchange, queue=queue_name)

# Delete file endwith .pkl in images directory
for file in os.listdir("./images"):
    if file.endswith(".pkl"):
        os.remove(os.path.join("./images", file))


# Define callback function to print incoming messages
def callback(ch, method, properties, body):
    print("Received")
    data = json.loads(body)
    frame = np.array(data["frame"], dtype=np.uint8)

    # convert timestamp from data['timestamp'] as utc time zone
    # convert utc time zone to local time zone
    timestamp = datetime.fromtimestamp(data["timestamp"], tz=pytz.utc).astimezone()

    # draw timestamp on frame at top right corner
    cv2.putText(
        frame,
        timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        (frame.shape[1] - 400, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )

    # save frame as image
    cv2.imwrite("frame.jpg", frame)

    # results = recognize(frame)

    # for result in results:
    #     if result.empty:
    #         cv2.imwrite("frame.jpg", frame)


# Start consuming messages
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
