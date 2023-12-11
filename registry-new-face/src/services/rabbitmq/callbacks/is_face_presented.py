import json
import os
from datetime import datetime
from uuid import uuid4

import cv2
import numpy as np
import pika
import pytz
from dotenv import load_dotenv
from src.constants import IMAGE_DIR
from src.database.models.dao.camera import CameraDAO
from src.database.models.dao.face import FaceDAO
from src.database.models.dao.person import PersonDAO
from src.logger import logger
from services.rabbitmq.blob import upload
from src.tasks.draw_info import draw_info
from src.tasks.recognize import recognize

# Environment variables
load_dotenv()
face_identification_exchange = os.environ.get("FACE_IDENTIFICATION_EXCHANGE", "face_identification")
hrm_queue = os.environ.get("HRM_QUEUE", "hrm_queue")
telegram_unknown_queue = os.environ.get("TELEGRAM_UNKNOWN_QUEUE", "telegram_unknown_queue")


def publish_hrm(ch, face_dict):
    ch.basic_publish(
        exchange=face_identification_exchange,
        routing_key=hrm_queue,
        body=json.dumps(face_dict),
        properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
    )
    logger.info(f"Published to {hrm_queue}")


def publish_telegram_unknown(ch, face_dict):
    ch.basic_publish(
        exchange=face_identification_exchange,
        routing_key=telegram_unknown_queue,
        body=json.dumps(face_dict),
        properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
    )
    logger.info(f"Published to {telegram_unknown_queue}")


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


def process_frame(ch, data):
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
            short_uuid = str(uuid4()).split("-", maxsplit=1)[0]
            row["name"] = f"UNKNOWN {short_uuid}"
            face_dict = save_to_database(row, frame, timestamp, camera_name)
            publish_telegram_unknown(ch, face_dict)
        else:
            face_dict = save_to_database(row, frame, timestamp, camera_name)
            publish_hrm(ch, face_dict)

        logger.info(f"Recognized: {row['name']}")


def callback(ch, method, properties, body):  # pylint: disable=unused-argument
    logger.info('[x] Received message "is_face_presented" queue')

    try:
        data = json.loads(body)
        process_frame(ch, data)
    except Exception as e:  # pylint: disable=broad-except, invalid-name
        logger.error(f"Error: {e}")
