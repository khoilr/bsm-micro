import json
import os
from datetime import datetime
import pika
import cv2
from dotenv import load_dotenv
from loguru import logger

from constants import FRAME_FREQUENCY, MAX_CAP_OPEN_FAILURES, MAX_READ_FRAME_FAILURES

load_dotenv()

# Environment variables
camera_url = os.environ.get("CAMERA_URL")
camera_info = os.environ.get("CAMERA_INFO")
rabbitmq_host = os.environ.get("RABBITMQ_HOST", "localhost")
rabbitmq_port = os.environ.get("RABBITMQ_PORT", 5672)
rabbitmq_username = os.environ.get("RABBITMQ_USERNAME", "guest")
rabbitmq_password = os.environ.get("RABBITMQ_PASSWORD", "guest")
rabbitmq_vhost = os.environ.get("RABBITMQ_VHOST", "/")
rabbitmq_exchange = os.environ.get("RABBITMQ_EXCHANGE", "frames")
rabbitmq_exchange_type = os.environ.get("RABBITMQ_EXCHANGE_TYPE", "fanout")

# Configure logger
logger.add(f"logs/{datetime.now().astimezone().isoformat()}.log", rotation="500 MB")

# RabbitMQ connection
credentials = pika.PlainCredentials(username=rabbitmq_username, password=rabbitmq_password)
parameters = pika.ConnectionParameters(rabbitmq_host, rabbitmq_port, "/", credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# RabbitMQ exchange
channel.exchange_declare(exchange=rabbitmq_exchange, exchange_type=rabbitmq_exchange_type)


def main():
    """Handle errors and restart the camera if necessary."""

    frame_counter = 0
    read_frame_failures_counter = 0
    cap_open_failures_counter = 0

    while cap_open_failures_counter < MAX_CAP_OPEN_FAILURES:
        cap = cv2.VideoCapture(camera_url)

        if not cap.isOpened():
            logger.error("Failed to connect to the camera.")
            cap_open_failures_counter += 1
            continue

        logger.info("Connected to the camera.")
        cap_open_failures_counter = 0
        read_frame_failures_counter = 0

        while read_frame_failures_counter < MAX_READ_FRAME_FAILURES:
            ret, frame = cap.read()

            if not ret:
                logger.error("Failed to capture frame.")
                read_frame_failures_counter += 1
                continue

            read_frame_failures_counter = 0
            frame_counter += 1

            if frame_counter % FRAME_FREQUENCY == 0:
                # Send to rabbitmq with camera info and current timestamp in second
                frame_info = {
                    "camera_info": camera_info,
                    "frame": frame.tolist(),
                    "timestamp": int(datetime.now().timestamp()),
                }
                channel.basic_publish(
                    exchange=rabbitmq_exchange,
                    routing_key="",
                    body=json.dumps(frame_info),
                )
                logger.info(f'Sent frame to exchange "{rabbitmq_exchange}".')

            if cv2.waitKey(1) == ord("q"):
                break

        logger.error(f"Read frame failures reached {MAX_READ_FRAME_FAILURES}. Restarting the camera...")

    logger.error(f"Capture open failures reached {MAX_CAP_OPEN_FAILURES}. Exiting the program...")


if __name__ == "__main__":
    main()
    connection.close()
