import os

from deepface import DeepFace

from constants import IMAGE_DIR
from logger import logger
from services.rabbitmq import RabbitMQ

# Create image dir
os.makedirs(IMAGE_DIR, exist_ok=True)

# Load VGG-Face model
DeepFace.build_model("VGG-Face")


def main():
    logger.info("Service started")

    rabbitmq = RabbitMQ()
    rabbitmq.consume()
    rabbitmq.close()


if __name__ == "__main__":
    main()
