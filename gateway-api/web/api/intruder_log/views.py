from datetime import datetime

from database.dao.intruderlog import LogDAO
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from web.api.utils import removeNoneParams

router = APIRouter(prefix="/intruderlog")


@router.get("/")
async def getAllLog():
    intruder_logs = await LogDAO.get_all()
    return JSONResponse(
        {"count": intruder_logs.__len__(), "data": [intruder_log.to_json() for intruder_log in intruder_logs]}
    )


@router.get("/{id}")
async def getLogByID(id: str):
    try:
        intruder_logID = int(id)
        intruder_log = await LogDAO.get(intruder_logID)
        if intruder_log:
            return JSONResponse(intruder_log.to_json())
        else:
            return JSONResponse(
                status_code=400,
                content={"status": 400, "msg": f'Not found intruder log with ID "{id}"'},
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
# async def createEvent(event: EventDTO):
#     try:
#         params = {
#             "description": event.name,
#         }
#         print(removeNoneParams(params=params))
#         createdEvent = await EventDAO.create(**removeNoneParams(params=params))
#         if createdEvent:
#             return JSONResponse(status_code=201, content=createdEvent.to_json())
#     except Exception as e:
#         return JSONResponse(
#             status_code=400, content={"status": 400, "msg": e.__str__()}
#         )

# @router.put("/{id}")
# async def updatePerson(person: EventDTO,id:str):
#     try:
#         personId = int(id)
#         params = {
#             "name": person.name,
#             "gender": person.gender,
#             "dob": person.dob,
#             "phone": person.phone,
#         }
#         print(removeNoneParams(params=params))
#         updatedPerson=await EventDAO.update(person_id=personId,**removeNoneParams(params))
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
#         deletedUser = await EventDAO.delete(person_id=personID)

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
