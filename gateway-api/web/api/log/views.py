import json
from typing import Optional

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from database.dao.event_log import EventLogDAO
from services.rabbitmq import CameraRPCClient
from web.api.utils import removeNoneParams

router = APIRouter(prefix="/log")


class LogDTO(BaseModel):
    video_url: str | None = Field(
        None,
    )
    image_id: str | None = Field(..., description="This field must not be empty")
    event: int | None = Field(None)
    face: int | None = Field(..., description="This field must not be empty")


@router.get("/")
async def getAllLog(limit: int = 20, offset: int = 0):
    camera_rpc_client = CameraRPCClient()
    results = camera_rpc_client.call(json.dumps({"name": "", "limit": limit, "offset": offset}))
    return JSONResponse(json.loads(results))


@router.get("/{name}")
async def getLogByName(name: str):
    camera_rpc_client = CameraRPCClient()
    results = camera_rpc_client.call(name)
    return JSONResponse(json.loads(results))


@router.post("/")
async def createLog(log: LogDTO):
    try:
        params = {
            "video_url": log.video_url,
            "image_id": log.image_id,
            "event_id": log.event,
            "face_id": log.face,
        }
        print(removeNoneParams(params=params))
        createdLog = await EventLogDAO.create(**removeNoneParams(params=params))
        if createdLog:
            return JSONResponse(status_code=201, content=createdLog.to_json())
    except Exception as e:
        return JSONResponse(status_code=400, content={"status": 400, "msg": e.__str__()})
