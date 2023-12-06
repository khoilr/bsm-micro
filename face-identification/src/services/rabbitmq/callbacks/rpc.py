import json

import pika

from src.database.models.dao.face import FaceDAO
from src.logger import logger


def callback(ch, method, props, body):
    logger.info('[x] Received message in "rpc" queue')

    data = json.loads(body)
    limit = data["limit"]
    offset = data["offset"]
    name = data["name"]

    if not name:
        faces = FaceDAO.get_all(limit=limit, offset=offset)
        faces = [face.to_dict() for face in faces]
    else:
        faces = FaceDAO.get_faces_by_camera_name(name)
        faces = [face.to_dict() for face in faces]

    ch.basic_publish(
        exchange="",
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=json.dumps(faces),
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)
