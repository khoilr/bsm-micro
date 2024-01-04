import json

import aio_pika
import numpy as np
from deepface import DeepFace

from src.logger import logger


async def handler(message: aio_pika.IncomingMessage, face_detection_exchange: aio_pika.Exchange):
    logger.info("[x] Received message from capture.frame")

    data = json.loads(message.body)
    frame = np.array(data, dtype=np.uint8)

    face_objects = DeepFace.extract_faces(img_path=frame, enforce_detection=False)
    face_objects = list(filter(lambda x: x["confidence"] > 0, face_objects))

    if len(face_objects) > 0:
        await face_detection_exchange.publish(
            aio_pika.Message(body=message.body),
            routing_key="",
        )
        logger.info("[x] Face is presented, publishing message")

    await message.ack()