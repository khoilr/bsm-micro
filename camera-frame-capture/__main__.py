import json
import os
from datetime import datetime

import cv2
import pika
from constants import (
    FRAME_FREQUENCY,
    MAX_CAP_OPEN_FAILURES,
    MAX_READ_FRAME_FAILURES,
    SEND_FRAME_FREQUENCY,
)
from dotenv import load_dotenv
from loguru import logger

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
rabbitmq_heartbeat_timeout = int(os.environ.get("RABBITMQ_HEARTBEAT_TIMEOUT", 600))

# Parse webcam (development)
try:
    camera_url = int(camera_url)
except ValueError:
    pass

# Configure logger
logger.add(f"logs/{datetime.now().astimezone().isoformat()}.log", rotation="500 MB")

# RabbitMQ connection
credentials = pika.PlainCredentials(username=rabbitmq_username, password=rabbitmq_password)
parameters = pika.ConnectionParameters(
    host=rabbitmq_host,
    port=rabbitmq_port,
    virtual_host="/",
    credentials=credentials,
    heartbeat=rabbitmq_heartbeat_timeout,
)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# RabbitMQ exchange
channel.exchange_declare(exchange=rabbitmq_exchange, exchange_type=rabbitmq_exchange_type)


def send_frame_to_rabbitmq(frame):
    """Send a frame to the RabbitMQ exchange."""
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


def main():
    """Handle errors and restart the camera if necessary."""
    cap_open_failures_counter = 0

    while cap_open_failures_counter < MAX_CAP_OPEN_FAILURES:
        cap = cv2.VideoCapture(camera_url)

        if not cap.isOpened():
            logger.error("Failed to connect to the camera.")
            cap_open_failures_counter += 1
            continue

        # Connect successfully
        logger.info("Connected to the camera.")
        read_frame_failures_counter = 0
        frames_counter = 1
        sent_frames_counter = 1

        while read_frame_failures_counter < MAX_READ_FRAME_FAILURES:
            ret, frame = cap.read()

            if not ret:
                logger.error("Failed to capture frame.")
                read_frame_failures_counter += 1
                continue

            # Capture successfully
            read_frame_failures_counter = 0

            # Increment frames_counter and sent_frames_counter
            if frames_counter % FRAME_FREQUENCY == 0:
                send_frame_to_rabbitmq(frame)

                # Reset cap if sent_frames_counter reaches SEND_FRAME_FREQUENCY
                if sent_frames_counter % SEND_FRAME_FREQUENCY == 0:
                    logger.info(f"Sent {SEND_FRAME_FREQUENCY} frames. Restarting the camera...")
                    cap.release()
                    cap = cv2.VideoCapture(camera_url)
                sent_frames_counter += 1

            frames_counter += 1

        logger.error(f"Read frame failures reached {MAX_READ_FRAME_FAILURES}. Restarting the camera...")

    logger.error(f"Capture open failures reached {MAX_CAP_OPEN_FAILURES}. Exiting the program...")


if __name__ == "__main__":
    main()
    connection.close()
