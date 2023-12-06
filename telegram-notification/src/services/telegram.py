import os
from typing import BinaryIO

import requests
from dotenv import load_dotenv

from src.constants import TELEGRAM_HOST

load_dotenv()
telegram_notification_bot_token = os.environ.get(
    "TELEGRAM_NOTIFICATION_BOT_TOKEN",
    "6417345389:AAF060Qcg9Bda_pbuALqGBPnW41QJz96Vho",
)
telegram_notification_chatid = os.environ.get("TELEGRAM_NOTIFICATION_CHATID", "-1002041653909")
blob_host = os.environ.get("BLOB_HOST", "localhost")
blob_port = os.environ.get("BLOB_PORT", "42000")

telegram_api = f"{TELEGRAM_HOST}/bot{telegram_notification_bot_token}"


def send_message(msg: str, attachment: BinaryIO = None):
    """Send telegram message to channel"""
    if attachment is not None:
        url = f"{telegram_api}/sendPhoto?chat_id={telegram_notification_chatid}"
        form_data = {"photo": attachment}
        result = requests.post(url=url, files=form_data, data={"caption": msg}, timeout=10)
    else:
        url = f"{telegram_api}/sendMessage?chat_id={telegram_notification_chatid}&text={msg}"
        result = requests.get(url=url, timeout=10)

    return result
