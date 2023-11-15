import json
from datetime import datetime

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from database.dao.camera import CameraDAO
from web.api.utils import removeNoneParams

router = APIRouter(prefix="/camera")


# class PersonDTO(BaseModel):
#     name: str = Field(..., description="This field must not be empty")
#     gender: int = Field(0)
#     dob: datetime | None = Field(None)
#     phone: str | None = Field(None)

import asyncio

from loguru import logger
from redis.asyncio import ConnectionPool, Redis

from services.redis.dependency import get_redis_pool


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
    # cameraDAO= CameraDao()
    # cameras = await Camera_Pydantic.from_queryset(CameraModel.all())
    cameras = await CameraDAO.get_all()
    return JSONResponse({"count": cameras.__sizeof__(), "data": [camera.to_json() for camera in cameras]})


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


# @router.post("/")
# async def createPerson(person: PersonDTO):
#     try:
#         params = {
#             "name": person.name,
#             "gender": person.gender,
#             "dob": person.dob,
#             "phone": person.phone,
#         }
#         print(removeNoneParams(params=params))
#         createdUser = await PersonDAO.create(**removeNoneParams(params=params))
#         if createdUser:
#             return JSONResponse(status_code=201, content=createdUser.to_json())
#     except Exception as e:
#         return JSONResponse(
#             status_code=400, content={"status": 400, "msg": e.__str__()}
#         )

# @router.put("/{id}")
# async def updatePerson(person: PersonDTO,id:str):
#     try:
#         personId = int(id)
#         params = {
#             "name": person.name,
#             "gender": person.gender,
#             "dob": person.dob,
#             "phone": person.phone,
#         }
#         print(removeNoneParams(params=params))
#         updatedPerson=await PersonDAO.update(person_id=personId,**removeNoneParams(params))
#         if updatedPerson:
#             return JSONResponse(status_code=200, content=updatedPerson.to_json())
#         else:
#             raise Exception('Not found person to update')
#     except Exception as e:
#         return JSONResponse(
#             status_code=400, content={"status": 400, "msg": e.__str__()}
#         )

# @router.delete("/{id}")
# async def deletePersonByID(id: str):
#     try:
#         personID=int(id)
#         deletedUser = await PersonDAO.delete(person_id=personID)

#         if deletedUser:
#             return JSONResponse(status_code=200, content={
#                 'status':200,
#                 'msg':f'Delete person with ID {id} succesfully'
#             })
#         else:
#             return JSONResponse(status_code=200, content={
#                 'status':200,
#                 'msg':'Not found person to delete'
#             })
#     except Exception as e:
#         return JSONResponse(
#             status_code=400, content={"status": 400, "msg": e.__str__()}
#         )
