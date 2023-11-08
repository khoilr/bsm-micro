import os
from datetime import datetime

import cv2
from dotenv import load_dotenv
from loguru import logger

from constants import FRAME_FREQUENCY, MAX_CAP_OPEN_FAILURES, MAX_READ_FRAME_FAILURES
from processors.identification import identify

load_dotenv()

# Environment variables
camera_url = os.environ.get("CAMERA_URL")
camera_info = os.environ.get("CAMERA_INFO")

# Configure logger
logger.add(f"logs/{datetime.now().astimezone().isoformat()}.log", rotation="500 MB")


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
                identify(frame)

            if cv2.waitKey(1) == ord("q"):
                break

        logger.error(f"Read frame failures reached {MAX_READ_FRAME_FAILURES}. Restarting the camera...")

    logger.error(f"Capture open failures reached {MAX_CAP_OPEN_FAILURES}. Exiting the program...")


if __name__ == "__main__":
    main()
