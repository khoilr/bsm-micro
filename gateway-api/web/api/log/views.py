from typing import Optional

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from database.dao.event_log import EventLogDAO
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
async def getAllLog(faceID: Optional[int] = None):
    logs = await EventLogDAO.get_all()
    if faceID:
        logs = [log for log in logs if (str(log.face) == str(faceID))]
    print([log.to_json() for log in logs])
    return JSONResponse({"count": logs.__len__(), "data": [log.to_json() for log in logs]})


@router.get("/{id}")
async def getLogByID(
    id: str,
):
    try:
        logID = int(id)
        log = await EventLogDAO.get(logID)
        if log:
            return JSONResponse(log.to_json())
        else:
            return JSONResponse(
                status_code=400,
                content={"status": 400, "msg": f"Not found log with ID '{id}'"},
            )
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "status": 400,
                "msg": e.__str__(),
            },
        )


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
