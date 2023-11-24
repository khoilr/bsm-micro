import os
from typing import BinaryIO
from dotenv import load_dotenv
from loguru import logger
import requests as rq
from datetime import datetime

load_dotenv("telegram_bot.env")

TELEGRAM_BOT_TOKEN = os.environ.get(
    "TELEGRAM_BOT_TOKEN", "6728691331:AAFbhSQ6Zt1FUO5nrq1tzJdE4rAygUUJIcw"
)
TELEGRAM_CHATID = os.environ.get("TELEGRAM_CHATID", "1002082538383")

DEFAULT_IMAGE_NAME = "image_name.jpg"


def downloadImageFile(url):
    img_data = rq.get(url=url).content
    with open(DEFAULT_IMAGE_NAME, "wb") as handler:
        handler.write(img_data)
    logger.info("Downloaded file from " + url)


def getUrlFromBlobID(id: str):
    # TODO: replace to env data later
    return f"http://103.157.218.126:42000/blob/{id}"


def sendTelegramMessage(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id=-{TELEGRAM_CHATID}&text={msg}"
    result = rq.get(url=url)
    return result


def sendTelegramPhotoUrlMsg(caption: str, filePath: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto?chat_id=-{TELEGRAM_CHATID}"

    formData = {
        "photo": filePath,
    }
    print(formData)
    result = rq.post(url=url, files=formData, data={"caption": caption})
    return result


def sendTelegramPhotoDataMsg(caption: str, filePath: BinaryIO):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto?chat_id=-{TELEGRAM_CHATID}"
    fileData = open(filePath, "rb")
    formData = {
        "photo": fileData,
    }
    print(formData)
    result = rq.post(url=url, files=formData, data={"caption": caption})
    return result


def handleSendMessageTelegram(data: any):
    personName = data["person_name"]
    if personName:
        # Unknow people
        detectedTime = datetime.fromtimestamp(int(data["created_at"]))
        fileUrl = getUrlFromBlobID(str(data["drew_image_url"]))
        try:
            if "unknow" in str(personName).lower():
                # download file to send
                downloadImageFile(fileUrl)

                # send message
                respond = sendTelegramPhotoDataMsg(
                    f"Có người lạ xuất hiện tại Zone 2 lúc {detectedTime.strftime('%Y/%m/%d, %H:%M:%S')}",
                    filePath=DEFAULT_IMAGE_NAME,
                )
                if respond.status_code == 200:
                    logger.success("[Telegram]: Sent message to Telegram - 200 OK")
                else:
                    raise Exception(f"Error sending message {str(respond.content)}")
                # remove file temp
                os.remove(DEFAULT_IMAGE_NAME)

            else:
                respond = sendTelegramMessage(
                    f"{personName} check-in lúc {detectedTime.strftime('%Y/%m/%d, %H:%M:%S')}",
                )
                if respond.status_code == 200:
                    logger.success("[Telegram]: Sent message to Telegram - 200 OK")
                else:
                    raise Exception(f"Error sending message {str(respond.content)}")
        except Exception as e:
            logger.error("[Telegram]: Error sending message to Telegram")
            logger.error(e)
