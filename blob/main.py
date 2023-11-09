import json
import os
import shutil
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Define a base path for uploads
UPLOADS_DIR = "uploads"
METADATA_FILE = "metadata.json"

# Mount the 'public' directory as a static asset
app.mount("/blob", StaticFiles(directory=UPLOADS_DIR), name="blob")


def create_upload_dir():
    Path(UPLOADS_DIR).mkdir(parents=True, exist_ok=True)


@app.on_event("startup")
async def on_startup():
    # Ensure the upload directory exists
    create_upload_dir()


@app.post("/upload/")
async def upload_file(file: UploadFile):
    create_upload_dir()

    original_name = file.filename
    stored_name = f"{datetime.now().timestamp()}_{original_name}"
    file_path = os.path.join(UPLOADS_DIR, stored_name)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    file_size = os.path.getsize(file_path)
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Store metadata in JSON file
    metadata = {
        "original_name": original_name,
        "stored_name": stored_name,
        "created_at": created_at,
        "file_size": file_size,
    }
    with open(METADATA_FILE, "a", encoding="utf-8") as json_file:
        json.dump(metadata, json_file)
        json_file.write("\n")

    return {
        "stored_name": stored_name,
        "original_name": original_name,
        "created_at": created_at,
        "file_size": file_size,
    }


@app.get("/download/{filename}")
async def download_file(filename: str):
    create_upload_dir()

    metadata = get_metadata(filename)
    if metadata:
        file_path = os.path.join(UPLOADS_DIR, filename)

        response = FileResponse(file_path)
        response.headers["Content-Disposition"] = f'attachment; filename="{metadata["original_name"]}"'
        return response
    else:
        raise HTTPException(status_code=404, detail="File not found")


@app.delete("/delete/{filename}")
async def delete_file(filename: str):
    create_upload_dir()

    metadata = get_metadata(filename)
    if metadata:
        file_path = os.path.join(UPLOADS_DIR, filename)

        try:
            os.remove(file_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete the file: {str(e)}")

        update_metadata_file(filename)
        return {"message": "File deleted"}
    else:
        raise HTTPException(status_code=404, detail="File not found")


def get_metadata(filename: str):
    with open(METADATA_FILE, "r", encoding="utf-8") as json_file:
        for line in json_file:
            metadata = json.loads(line)
            if metadata["stored_name"] == filename:
                return metadata
    return None


def update_metadata_file(filename: str):
    with open(METADATA_FILE, "r", encoding="utf-8") as json_file:
        lines = json_file.readlines()
    with open(METADATA_FILE, "w", encoding="utf-8") as json_file:
        for line in lines:
            metadata = json.loads(line)
            if metadata["stored_name"] != filename:
                json_file.write(line)
