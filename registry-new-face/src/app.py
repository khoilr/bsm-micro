import os

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse

from src.services.rabbitmq import RabbitMQ
from src.services.rabbitmq.blob import upload

app = FastAPI()


@app.post("/registry")
async def registry(name: str = Form(...), video: UploadFile = File(...)):
    rabbitmq = RabbitMQ()

    # Save file to local
    video_content = await video.read()
    file_name = video.filename
    local_file_name = f"temp/{file_name}"
    with open(local_file_name, "wb") as f:
        f.write(video_content)

    # upload to blob
    video_blob = upload(local_file_name)

    # remove video
    os.remove(local_file_name)

    # publish to rabbitmq
    message = {
        "name": name,
        "video": video_blob,
    }
    rabbitmq.publish(message)

    return JSONResponse(status_code=200, content=message)
