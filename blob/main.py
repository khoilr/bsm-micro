import os
import shutil
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from models import StorageDAO
from database import Session

# Define a base path for uploads
UPLOADS_DIR = "uploads"

# Create database session
session = Session()


def create_upload_dir():
    Path(UPLOADS_DIR).mkdir(parents=True, exist_ok=True)


create_upload_dir()

app = FastAPI()
# Mount the 'public' directory as a static asset
app.mount("/blob", StaticFiles(directory=UPLOADS_DIR), name="blob")


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

    StorageDAO.create(
        original_name=original_name,
        stored_name=stored_name,
        created_at=created_at,
        file_size=file_size,
    )

    return {
        "stored_name": stored_name,
        "original_name": original_name,
        "created_at": created_at,
        "file_size": file_size,
    }


@app.get("/download/{filename}")
async def download_file(filename: str):
    create_upload_dir()

    metadata = StorageDAO.get(filename)
    if metadata:
        file_path = os.path.join(UPLOADS_DIR, filename)

        response = FileResponse(file_path)
        response.headers[
            "Content-Disposition"
        ] = f'attachment; filename="{metadata["original_name"]}"'
        return response
    else:
        raise HTTPException(status_code=404, detail="File not found")


@app.delete("/delete/{filename}")
async def delete_file(filename: str):
    create_upload_dir()

    metadata = StorageDAO.get(filename)
    if metadata:
        file_path = os.path.join(UPLOADS_DIR, filename)

        try:
            os.remove(file_path)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to delete the file: {str(e)}"
            )

        StorageDAO.delete(filename)
        return {"message": "File deleted"}
    else:
        raise HTTPException(status_code=404, detail="File not found")
