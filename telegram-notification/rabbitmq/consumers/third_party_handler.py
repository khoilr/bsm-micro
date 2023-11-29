import json

from rabbitmq.consumers.hrm_check_in import handleDataHRM
from rabbitmq.consumers.telegram_message_send import send_telegram_message
from logger import logger


def callback(channel, method, properties, body):
    logger.info(f" [x] Received {body}")

    # Load data from body
    data = json.loads(body)

    # handle message send to telegram
    send_telegram_message(data=data)

    # handle data send to HRM
    handleDataHRM(data=data)
