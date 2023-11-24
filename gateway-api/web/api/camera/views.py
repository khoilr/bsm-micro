import random
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from database.dao.camera import CameraDAO
from pydantic import BaseModel, Field
from datetime import datetime
from server.web.api.utils import removeNoneParams
from loguru import logger


router = APIRouter(prefix="/camera")


class CameraBaseDTO(BaseModel):
    # name: str | None = Field(
    #     default="Camera " + int(datetime.now().timestamp() / 1000),
    # )
    description: str | None = Field(None)
    connect_uri: str | None = Field(None)
    placeholder_url: str | None = Field(None)
    type: int | None = Field(None)
    zone_id: int | None = Field(None)


class CameraCreateDTO(CameraBaseDTO):
    name: str | None = Field(
        default="Camera " + str(int(datetime.now().timestamp() / 1000)),
    )


class CameraUpdateDTO(CameraBaseDTO):
    name: str | None = Field(None)


# @router.get("/blabla")
# async def listen_for_changes(app: FastAPI, polling_interval: int = 1):
#     prev_value = None
#     redis_pool =   app.state.redis_pool
#     async with Redis(connection_pool=redis_pool) as redis:
#         while True:
#             current_value = await redis.get('key')
#             if prev_value != current_value:
#                 logger.info(f"Value changed to: {current_value}")
#                 prev_value = current_value
#             else:
#                 logger.info(f"No changes detected")
@router.get("/")
async def getAllCamera():
    cameras = await CameraDAO.get_all()
    return JSONResponse(
        {
            "count": len(cameras),
            "data": [camera.to_json() for camera in cameras],
        }
    )


@router.get("/{id}")
async def getCameraByID(id: str):
    try:
        cameraID = int(id)
        camera = await CameraDAO.get(cameraID)
        if camera:
            return JSONResponse(camera.to_json())
        else:
            return JSONResponse(
                status_code=400,
                content={"status": 400, "msg": f'Not found camera with ID "{id}"'},
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
async def createCamera(camera: CameraCreateDTO):
    try:
        params = {
            "name": camera.name,
            "description": camera.description,
            "connect_uri": camera.connect_uri,
            "placeholder_url": camera.placeholder_url,
            "type": camera.type,
            "zone_id": camera.zone_id,
        }
        logger.info(removeNoneParams(params=params))
        createdCamera = await CameraDAO.create(**removeNoneParams(params=params))
        if createdCamera:
            return JSONResponse(status_code=201, content=createdCamera.to_json())
    except Exception as e:
        return JSONResponse(
            status_code=400, content={"status": 400, "msg": e.__str__()}
        )


@router.put("/{id}")
async def updateCamera(camera: CameraUpdateDTO, id: str):
    try:
        cameraID = int(id)
        params = {
            "name": camera.name,
            "description": camera.description,
            "connect_uri": camera.connect_uri,
            "placeholder_url": camera.placeholder_url,
            "type": camera.type,
            "zone_id": camera.zone_id,
        }
        logger.info(removeNoneParams(params=params))
        updatedCamera = await CameraDAO.update(
            camera_id=cameraID, **removeNoneParams(params)
        )
        if updatedCamera:
            return JSONResponse(status_code=200, content=updatedCamera.to_json())
        else:
            raise Exception("Not found camera to update")
    except Exception as e:
        return JSONResponse(
            status_code=400, content={"status": 400, "msg": e.__str__()}
        )


@router.delete("/{id}")
async def deleteCameraByID(id: str):
    try:
        cameraID = int(id)
        deletedCamera = await CameraDAO.delete(camera_id=cameraID)

        if deletedCamera:
            return JSONResponse(
                status_code=200,
                content={
                    "status": 200,
                    "msg": f"Delete camera with ID '{id}' succesfully",
                },
            )
        else:
            return JSONResponse(
                status_code=200,
                content={"status": 200, "msg": "Not found person to delete"},
            )
    except Exception as e:
        return JSONResponse(
            status_code=400, content={"status": 400, "msg": e.__str__()}
        )
