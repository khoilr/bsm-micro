import os

import requests
from dotenv import load_dotenv

from src.constants import IMAGE_NAME
from src.logger import logger

load_dotenv()
BLOB_HOST = os.environ.get("BLOB_HOST", "localhost")
BLOB_PORT = os.environ.get("BLOB_PORT", "42000")


def download_image_file(url):
    """Download image and save to disk"""
    try:
        img_data = requests.get(url=url, timeout=10).content
        with open(IMAGE_NAME, "wb") as handler:
            handler.write(img_data)
    except requests.RequestException as e:
        logger.error(f"Error downloading image: {e}")


def get_blob_url(blob_id: str):
    """Get blob url from blob id"""
    return f"http://{BLOB_HOST}:{BLOB_PORT}/blob/{blob_id}"
