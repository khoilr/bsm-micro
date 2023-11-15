import pika
from database.models.dao.faces import FaceDAO
import json


# Define a function to handle requests and return responses
def callback(ch, method, props, body):
    faces = FaceDAO.get_faces_by_camera(str(body))
    faces = [face.__dict__ for face in faces]

    ch.basic_publish(
        exchange="",
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=json.dumps(faces),
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)
