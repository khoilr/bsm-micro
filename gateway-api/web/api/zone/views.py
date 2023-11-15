from datetime import datetime

from database.dao.zone import ZoneDAO
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from web.api.utils import removeNoneParams

router = APIRouter(prefix="/zone")


# class PersonDTO(BaseModel):
#     name: str = Field(..., description="This field must not be empty")
#     gender: int = Field(0)
#     dob: datetime | None = Field(None)
#     phone: str | None = Field(None)


@router.get("/")
async def getAllZone():
    zones = await ZoneDAO.get_all()
    return JSONResponse({"count": zones.__len__(), "data": [zone.to_json() for zone in zones]})


@router.get("/{id}")
async def getCameraByID(id: str):
    try:
        zoneID = int(id)
        zone = await ZoneDAO.get(zoneID)
        if zone:
            return JSONResponse(zone.to_json())
        else:
            return JSONResponse(
                status_code=400,
                content={"status": 400, "msg": f'Not found zone with ID "{id}"'},
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
