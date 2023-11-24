from fastapi import APIRouter
from fastapi.responses import JSONResponse
from database.dao.person import PersonDAO
from pydantic import BaseModel, Field
from datetime import datetime
from server.web.api.utils import removeNoneParams

router = APIRouter(prefix="/people")


class PersonDTO(BaseModel):
    name: str | None = Field(None)
    gender: int = Field(0)
    dob: datetime | None = Field(None)
    phone: str | None = Field(None)
    avatar_url: str | None = Field(None)
    position: str | None = Field(None)


@router.get("/")
async def getAllPeople():
    people = await PersonDAO.get_all()
    print([person.to_json() for person in people])
    return JSONResponse(
        {"count": people.__len__(), "data": [person.to_json() for person in people]}
    )


@router.get("/{id}")
async def getPersonByID(id: str):
    try:
        personId = int(id)
        person = await PersonDAO.get(personId)
        if person:
            return JSONResponse(person.to_json())
        else:
            return JSONResponse(
                status_code=400,
                content={"status": 400, "msg": f'Not found user with ID "{id}"'},
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
async def createPerson(person: PersonDTO):
    try:
        params = {
            "name": person.name,
            "gender": person.gender,
            "dob": person.dob,
            "phone": person.phone,
            "avatar_url": person.avatar_url,
            "position": person.position,
        }
        print(removeNoneParams(params=params))
        createdUser = await PersonDAO.create(**removeNoneParams(params=params))
        if createdUser:
            return JSONResponse(status_code=201, content=createdUser.to_json())
    except Exception as e:
        return JSONResponse(
            status_code=400, content={"status": 400, "msg": e.__str__()}
        )


@router.put("/{id}")
async def updatePerson(person: PersonDTO, id: str):
    try:
        personId = int(id)
        params = {
            "name": person.name,
            "gender": person.gender,
            "dob": person.dob,
            "phone": person.phone,
            "avatar_url": person.avatar_url,
            "position": person.position,
        }
        updatedPerson = await PersonDAO.update(
            person_id=personId, **removeNoneParams(params)
        )
        print(updatedPerson.to_json())
        if updatedPerson:
            return JSONResponse(status_code=200, content=updatedPerson.to_json())
        else:
            raise Exception("Not found person to update")
    except Exception as e:
        return JSONResponse(
            status_code=400, content={"status": 400, "msg": e.__str__()}
        )


@router.delete("/{id}")
async def deletePersonByID(id: str):
    try:
        personID = int(id)
        deletedUser = await PersonDAO.delete(person_id=personID)

        if deletedUser:
            return JSONResponse(
                status_code=200,
                content={
                    "status": 200,
                    "msg": f"Delete person with ID '{id}' succesfully",
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
