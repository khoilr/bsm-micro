import json
import os
from datetime import datetime

from src.constants import IMAGE_NAME
from src.logger import logger
from src.services.file import download_image_file, get_blob_url
from src.services.telegram import send_message


def send_telegram_message(data: any):
    completed = data["completed"]
    if completed:
        time = datetime.fromtimestamp(int(data["checkout_at"]))
        file_url = get_blob_url(str(data["checkout_img"]))
        message = f"{data['employee_name']} đã check out lúc {time.strftime('%Y/%m/%d, %H:%M:%S')}"
    else:
        time = datetime.fromtimestamp(int(data["checkin_at"]))
        file_url = get_blob_url(str(data["checkin_img"]))
        message = f"{data['employee_name']} đã check out lúc {time.strftime('%Y/%m/%d, %H:%M:%S')}"

    download_image_file(file_url)

    try:
        # Send message
        with open(IMAGE_NAME, "rb") as image_file:
            respond = send_message(
                message,
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


def callback(channel, method, properties, body):
    logger.info(f" [x] Received message from {method.routing_key}")

    try:
        data = json.loads(body)
        send_telegram_message(data)
    except json.JSONDecodeError as je:
        logger.error(f"JSONDecodeError: {je}")
    except Exception as ex:
        logger.error(f"Exception occurred: {ex}")
