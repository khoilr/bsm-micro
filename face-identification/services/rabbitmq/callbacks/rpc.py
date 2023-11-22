import json

import pika

from database.models.dao.face import FaceDAO


def callback(ch, method, props, body):
    body = body.decode("utf-8")
    print(body, bool(body))
    if not body:
        faces = FaceDAO.get_all()
        faces = [face.to_dict() for face in faces]
    else:
        faces = FaceDAO.get_faces_by_camera_name(body)
        faces = [face.to_dict() for face in faces]

    ch.basic_publish(
        exchange="",
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=json.dumps(faces),
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)
