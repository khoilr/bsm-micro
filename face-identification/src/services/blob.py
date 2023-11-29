import os

import requests
from dotenv import load_dotenv

load_dotenv()

blob_host = os.environ.get("BLOB_HOST", "localhost")
blob_port = os.environ.get("BLOB_PORT", 8000)
blob_scheme = os.environ.get("BLOB_SCHEME", "http")


def upload(file_path: str):
    try:
        method = "post"
        url = f"{blob_scheme}://{blob_host}:{blob_port}/upload"
        files = {"file": open(file=file_path, mode="rb")}
        response = requests.request(method, url, files=files, timeout=10)
        url = response.json()
        return url
    except Exception:  # pylint: disable=broad-except
        return {"stored_name": ""}
