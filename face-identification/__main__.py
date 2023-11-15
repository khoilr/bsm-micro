import os

from constants import IMAGE_DIR
from services.logger import logger
from services.rabbitmq import RabbitMQ

# Create image dir
os.makedirs(IMAGE_DIR, exist_ok=True)


def main():
    logger.info("Service started")

    rabbitmq = RabbitMQ()
    rabbitmq.consume()
    rabbitmq.close()


if __name__ == "__main__":
    main()
