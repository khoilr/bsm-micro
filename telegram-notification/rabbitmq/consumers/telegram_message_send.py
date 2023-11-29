import os
from datetime import datetime
from typing import BinaryIO

import requests
from dotenv import load_dotenv

from constants import IMAGE_NAME, TELEGRAM_HOST
from logger import logger

load_dotenv()
TELEGRAM_NOTIFICATION_BOT_TOKEN = os.environ.get(
    "TELEGRAM_NOTIFICATION_BOT_TOKEN",
    "6417345389:AAF060Qcg9Bda_pbuALqGBPnW41QJz96Vho",
)
TELEGRAM_NOTIFICATION_CHATID = os.environ.get("TELEGRAM_NOTIFICATION_CHATID", "-1002041653909")
BLOB_HOST = os.environ.get("BLOB_HOST", "localhost")
BLOB_PORT = os.environ.get("BLOB_PORT", "42000")

print(TELEGRAM_NOTIFICATION_CHATID)

telegram_api = f"{TELEGRAM_HOST}/bot{TELEGRAM_NOTIFICATION_BOT_TOKEN}"


def download_image_file(url):
    """Download image and save to disk"""
    img_data = requests.get(url=url, timeout=10).content

    with open(IMAGE_NAME, "wb") as handler:
        handler.write(img_data)


def get_blob_url(blob_id: str):
    """Get blob url from blob id"""
    return f"http://{BLOB_HOST}:{BLOB_PORT}/blob/{blob_id}"


def send_message(msg: str, attachment: BinaryIO = None):
    """Send telegram message to channel"""
    if attachment is not None:
        url = f"{telegram_api}/sendPhoto?chat_id={TELEGRAM_NOTIFICATION_CHATID}"
        form_data = {"photo": attachment}
        result = requests.post(url=url, files=form_data, data={"caption": msg}, timeout=10)
    else:
        url = f"{telegram_api}/sendMessage?chat_id={TELEGRAM_NOTIFICATION_CHATID}&text={msg}"
        result = requests.get(url=url, timeout=10)

    return result


def send_telegram_message(data: any):
    """Send message to telegram"""

    person_name = data["person_name"]
    if person_name:
        # Parse
        detected_time = datetime.fromtimestamp(int(data["created_at"]))

        # Donwload file to local
        file_url = get_blob_url(str(data["drew_image_url"]))
        download_image_file(file_url)

        try:
            # Send message
            with open(IMAGE_NAME, "rb") as image_file:
                respond = send_message(
                    f"Có người lạ xuất hiện tại Zone 2 lúc {detected_time.strftime('%Y/%m/%d, %H:%M:%S')}"
                    if "unknow" in str(person_name).lower()
                    else f"{person_name} check-in lúc {detected_time.strftime('%Y/%m/%d, %H:%M:%S')}",
                    attachment=image_file,
                )

            # Handle response
            if respond.status_code == 200:
                logger.success("[Telegram]: Sent message to Telegram")
            else:
                raise Exception(f"Error sending message {str(respond.content)}")

            # Remove file temp
            os.remove(IMAGE_NAME)

        except Exception as e:  # pylint: disable=broad-except,invalid-name
            logger.error("[Telegram]: Error sending message to Telegram")
            logger.error(e)
