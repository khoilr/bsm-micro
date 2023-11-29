from src.logger import logger
from src.rabbitmq import RabbitMQ


def app():
    logger.info("Is Face Presented Service Started")
    rabbitmq = RabbitMQ()
    rabbitmq.consume()
    rabbitmq.close()
