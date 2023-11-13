import json
import os
from datetime import datetime

import cv2
import numpy as np
import pytz

from constants import IMAGE_DIR
from logger import logger
from processors.draw_info import draw_info
from processors.recognize import recognize
from rabbitmq import RabbitMQ

# # Create image dir
# os.makedirs(IMAGE_DIR, exist_ok=True)

# # Delete file endwith .pkl in images directory
# for file in os.listdir(IMAGE_DIR):
#     if file.endswith(".pkl"):
#         os.remove(os.path.join(IMAGE_DIR, file))


# Define callback function to print incoming messages
def callback(ch, method, properties, body):  # pylint: disable=unused-argument
    logger.info("[x] Received message")

    data = json.loads(body)
    frame = np.array(data["frame"], dtype=np.uint8)
    timestamp = datetime.fromtimestamp(data["timestamp"], tz=pytz.utc).astimezone()
    camera_info = data["camera_info"]

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

    # draw camera info on frame at bottom left corner
    cv2.putText(
        frame,
        camera_info,
        (50, frame.shape[0] - 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )

    # save frame as image
    cv2.imwrite("frame.jpg", frame)

    results = recognize(frame)

    for result in results:
        if not result.empty:
            name_counts = result["name"].value_counts()
            most_common_name = name_counts.idxmax()
            appearance_times = name_counts.max()
            row = result[result["name"] == most_common_name]

            image = draw_info(frame, row)

            cv2.imwrite("frame_box.jpg", image)

            if appearance_times < 3:
                row["name"] = "Unknown"

            image = draw_info(frame, row)


def main():
    rabbitmq = RabbitMQ()
    rabbitmq.consume(on_message_callback=callback)
    rabbitmq.close()


if __name__ == "__main__":
    main()
