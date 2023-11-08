import json
import os
from datetime import datetime

import cv2
import redis
from dotenv import load_dotenv
from loguru import logger

from constants import FRAME_FREQUENCY, MAX_CAP_OPEN_FAILURES, MAX_READ_FRAME_FAILURES

load_dotenv()

# Environment variables
camera_url = os.environ.get("CAMERA_URL")
camera_info = os.environ.get("CAMERA_INFO")
redis_host = os.environ.get("REDIS_HOST", "localhost")
redis_port = os.environ.get("REDIS_PORT", 6379)
redis_key = os.environ.get("REDIS_KEY", "frames")

# Configure logger
logger.add(f"logs/{datetime.now().astimezone().isoformat()}.log", rotation="500 MB")

# Redis server configuration
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0)


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
                redis_client.xadd(
                    name=redis_key,
                    fields={"frame": json.dumps(frame.tolist()), "camera_info": camera_info},
                    maxlen=1,
                )
                logger.info(f'Frame sent to the stream "{redis_key}".')

            if cv2.waitKey(1) == ord("q"):
                break

        logger.error(f"Read frame failures reached {MAX_READ_FRAME_FAILURES}. Restarting the camera...")

    logger.error(f"Capture open failures reached {MAX_CAP_OPEN_FAILURES}. Exiting the program...")


if __name__ == "__main__":
    main()
    redis_client.close()
