import json
import os
from datetime import datetime
from uuid import uuid4
import cv2
import numpy as np
import pytz
from dotenv import load_dotenv

from constants import IMAGE_DIR, KNOWN_THRESHOLD, UNKNOWN_THRESHOLD
from database.models.dao.camera import CameraDAO
from database.models.dao.face import FaceDAO
from database.models.dao.person import PersonDAO
from logger import logger
from services.blob import upload
from tasks.draw_info import draw_info
from tasks.recognize import recognize

# Environment variables
load_dotenv()
face_identification_exchange = os.environ.get("FACE_IDENTIFICATION_EXCHANGE", "face_identification")
face_identification_queue = os.environ.get("FACE_IDENTIFICATION_QUEUE", "face_identification")


def publish(ch, face_dict):
    ch.basic_publish(
        exchange=face_identification_exchange,
        routing_key=face_identification_queue,
        body=json.dumps(face_dict),
    )


def save_to_database(row, image, timestamp, camera_name):
    # Save frame and image into temp files
    drew_image = draw_info(image, row)

    image_temp = os.path.join(IMAGE_DIR, "image.jpg")
    drew_image_temp = os.path.join(IMAGE_DIR, "drew_image.jpg")

    cv2.imwrite(image_temp, image)
    cv2.imwrite(drew_image_temp, drew_image)

    image_blob = upload(image_temp)
    drew_image_blob = upload(drew_image_temp)

    # Insert to database: camera (create if not exists), person (create if not exists), face
    camera = CameraDAO.insert_or_get(camera_name)
    person = PersonDAO.insert_or_get(row["name"])
    face = FaceDAO.insert_or_get(
        x=row["source_x"],
        y=row["source_y"],
        w=row["source_w"],
        h=row["source_h"],
        image_url=image_blob["stored_name"],
        drew_image_url=drew_image_blob["stored_name"],
        camera_id=camera.id,
        person_id=person.id,
        created_at=timestamp,
    )

    # Delete temp files
    os.remove(image_temp)
    os.remove(drew_image_temp)

    return face.to_dict()


def process_frame(data, ch):
    frame = np.array(data["frame"], dtype=np.uint8)
    timestamp = datetime.fromtimestamp(data["timestamp"], tz=pytz.utc).astimezone()
    camera_name = data["camera_name"]

    # Save frame to a temp file
    results = recognize(frame)

    for result in results:
        if result.empty:
            continue

        name_counts = result["name"].value_counts()
        most_common_name = name_counts.idxmax()

        row = result[result["name"] == most_common_name].iloc[0].to_dict()

        if name_counts[most_common_name] < 2:
            #     for name, count in name_counts.items():
            #         if name == most_common_name:
            #             continue

            #         if count > UNKNOWN_THRESHOLD:
            #             short_uuid = str(uuid4()).split("-", maxsplit=1)[0]
            #             row["name"] = f"UNKNOWN {short_uuid}"
            #             break
            # else:
            short_uuid = str(uuid4()).split("-", maxsplit=1)[0]
            row["name"] = f"UNKNOWN {short_uuid}"

        logger.info(f"Recognized: {row['name']}")

        face_dict = save_to_database(row, frame, timestamp, camera_name)
        publish(
            ch,
            face_dict,
        )


def callback(ch, method, properties, body):  # pylint: disable=unused-argument
    logger.info('[x] Received message "is_face_presented" queue')

    try:
        data = json.loads(body)
        process_frame(data, ch)
    except Exception as e:
        logger.error(f"Error: {e}")

    # # Get data from message
    # data = json.loads(body)
    # frame = np.array(data["frame"], dtype=np.uint8)
    # timestamp = datetime.fromtimestamp(data["timestamp"], tz=pytz.utc).astimezone()
    # camera_name = data["camera_name"]

    # # Save frame to a temp file
    # results = recognize(frame)

    # for result in results:
    #     if result.empty:
    #         continue

    #     name_counts = result["name"].value_counts()
    #     most_common_name = name_counts.idxmax()

    #     row = result[result["name"] == most_common_name].iloc[0].to_dict()

    #     if name_counts[most_common_name] >= KNOWN_THRESHOLD:
    #         for name, count in name_counts.items():
    #             if name == most_common_name:
    #                 continue

    #             if count > UNKNOWN_THRESHOLD:
    #                 short_uuid = str(uuid4()).split("-", maxsplit=1)[0]
    #                 result.loc[result["name"] == name, "name"] = f"UNKNOWN {short_uuid}"
    #                 break
    #     else:
    #         short_uuid = str(uuid4()).split("-", maxsplit=1)[0]
    #         row["name"] = f"UNKNOWN {short_uuid}"

    #     image = draw_info(frame, row)

    #     # Save frame and image into temp files
    #     frame_temp = os.path.join(IMAGE_DIR, "frame.jpg")
    #     image_temp = os.path.join(IMAGE_DIR, "image.jpg")

    #     cv2.imwrite(frame_temp, frame)
    #     cv2.imwrite(image_temp, image)

    #     frame_blob = upload(frame_temp)
    #     image_blob = upload(image_temp)

    #     # Insert to database: camera (create if not exists), person (create if not exists), face
    #     camera = CameraDAO.insert_or_get(camera_name)
    #     person = PersonDAO.insert_or_get(row["name"])
    #     face = FaceDAO.insert_or_get(
    #         x=row["source_x"],
    #         y=row["source_y"],
    #         w=row["source_w"],
    #         h=row["source_h"],
    #         image_url=frame_blob["stored_name"],
    #         drew_image_url=image_blob["stored_name"],
    #         camera_id=camera.id,
    #         person_id=person.id,
    #         created_at=timestamp,
    #     )

    #     logger.info(f"Face {row['name']} detected")

    #     # Delete temp files
    #     os.remove(frame_temp)
    #     os.remove(image_temp)

    #     # publish to exchange
    #     publish_data = face.to_dict()
    #     ch.basic_publish(
    #         exchange=face_identification_exchange,
    #         routing_key=face_identification_queue,
    #         body=json.dumps(publish_data),
    #     )
