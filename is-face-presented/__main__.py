from logger import logger
from rabbitmq import RabbitMQ


def main():
    logger.info("Is Face Presented Service Started")
    rabbitmq = RabbitMQ()
    rabbitmq.consume()
    rabbitmq.close()


if __name__ == "__main__":
    main()
