import json
import os
from datetime import datetime

import cv2
import numpy as np
import pytz

from constants import IMAGE_DIR
from database.models.dao.camera import CameraDAO
from database.models.dao.faces import FaceDAO
from database.models.dao.person import PersonDAO
from processors.draw_info import draw_info
from processors.recognize import recognize
from services.blob import upload
from services.logger import logger


def callback(ch, method, properties, body):  # pylint: disable=unused-argument
    logger.info("[x] Received message")

    # Get data from message
    data = json.loads(body)
    frame = np.array(data["frame"], dtype=np.uint8)
    timestamp = datetime.fromtimestamp(data["timestamp"], tz=pytz.utc).astimezone()
    camera_info = data["camera_info"]

    # Save frame to a temp file
    results = recognize(frame)

    for result in results:
        if not result.empty:
            name_counts = result["name"].value_counts()
            most_common_name = name_counts.idxmax()
            appearance_times = name_counts.max()
            row = result[result["name"] == most_common_name]

            if appearance_times < 3:
                row["name"] = "Unknown"

            image = draw_info(frame, row)

            # Save frame and image into temp files
            frame_temp = os.path.join(IMAGE_DIR, "frame.jpg")
            image_temp = os.path.join(IMAGE_DIR, "image.jpg")

            cv2.imwrite(frame_temp, frame)
            cv2.imwrite(image_temp, image)

            frame_blob = upload(frame_temp)
            image_blob = upload(image_temp)

            # Insert to database: camera (create if not exists), person (create if not exists), face
            camera = CameraDAO.insert_or_get(camera_info)
            person = PersonDAO.insert_or_get(row["name"])
            FaceDAO.insert_or_get(
                x=row["source_x"],
                y=row["source_y"],
                width=row["source_w"],
                height=row["source_h"],
                image_url=frame_blob["stored_name"],
                drew_image_url=image_blob["stored_name"],
                camera_id=camera.id,
                person_id=person.id,
            )

            logger.info(f"Face {row['name']} detected")

            # Delete temp files
            os.remove(frame_temp)
            os.remove(image_temp)
