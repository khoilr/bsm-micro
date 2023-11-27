import json
from rabbitmq.consumers.telegram_message_send import handleSendMessageTelegram
from rabbitmq.consumers.hrm_check_in import handleDataHRM


def callback(channel, method, properties, body):
    # logger.info("Receive message")
    # load data receive
    data = json.loads(body)

    # handle message send to telegram
    handleSendMessageTelegram(data=data)

    # handle data send to HRM
    handleDataHRM(data=data)
