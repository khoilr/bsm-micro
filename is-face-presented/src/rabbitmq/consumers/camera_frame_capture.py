import json
import os

import numpy as np
import pika
from deepface import DeepFace
from dotenv import load_dotenv

from src.logger import logger

# Environment variables
load_dotenv()
is_face_presented_exchange = os.environ.get("IS_FACE_PRESENTED_EXCHANGE", "is_face_presented")


def callback(ch, method, properties, body):  # pylint: disable=unused-argument
    logger.info("[x] Received message")
    data = json.loads(body)

    frame = np.array(data["frame"], dtype=np.uint8)
    face_objects = DeepFace.extract_faces(img_path=frame, enforce_detection=False)
    face_objects = list(filter(lambda x: x["confidence"] > 0, face_objects))

    if len(face_objects) > 0:
        ch.basic_publish(
            exchange=is_face_presented_exchange,
            routing_key="",
            body=body,
            properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE),
        )
        logger.info("[x] Face is presented, publishing message")
