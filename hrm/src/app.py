from src.services.rabbitmq import RabbitMQ


def app():
    rabbitmq = RabbitMQ()
    rabbitmq.consume()
    rabbitmq.close()
