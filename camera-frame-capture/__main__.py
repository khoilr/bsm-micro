import json
import os
from datetime import datetime

import cv2
from dotenv import load_dotenv

from constants import (
    FRAME_FREQUENCY,
    MAX_CAP_OPEN_FAILURES,
    MAX_READ_FRAME_FAILURES,
    SEND_FRAME_FREQUENCY,
    COMPRESS_WIDTH,
)
from logger import logger
from rabbitmq import RabbitMQ

# Environment variables
load_dotenv()
camera_url = os.environ.get("CAMERA_FRAME_CAPTURE_CAMERA_URL")
camera_name = os.environ.get("CAMERA_FRAME_CAPTURE_CAMERA_NAME")

# Parse webcam (development)
try:
    camera_url = int(camera_url)
except ValueError:
    pass

# Init RabbitMQ
rabbitmq = RabbitMQ()


def send_frame_to_rabbitmq(frame):
    """Send a frame to the RabbitMQ exchange."""
    frame_info = {
        "camera_name": camera_name,
        "frame": frame.tolist(),
        "timestamp": int(datetime.now().timestamp()),
    }
    rabbitmq.send(json.dumps(frame_info))


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
                frame = cv2.resize(frame, (COMPRESS_WIDTH, int(COMPRESS_WIDTH * 9 / 16)))
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
    rabbitmq.close()
