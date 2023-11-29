import os

from deepface import DeepFace

from src.constants import IMAGE_DIR
from src.logger import logger
from src.services.rabbitmq import RabbitMQ


def app():
    # Create image dir
    os.makedirs(IMAGE_DIR, exist_ok=True)

    # Remove pkl files in IMAGE_DIR
    for file in os.listdir(IMAGE_DIR):
        if file.endswith(".pkl"):
            os.remove(os.path.join(IMAGE_DIR, file))

    # Load VGG-Face model
    DeepFace.build_model("Facenet512")

    logger.info("Service started")

    rabbitmq = RabbitMQ()
    rabbitmq.consume()
    rabbitmq.close()
