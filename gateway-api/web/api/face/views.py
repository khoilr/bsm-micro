from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from database.dao.face import FaceDAO
from web.api.utils import removeNoneParams

router = APIRouter(prefix="/face")


class FaceDTO(BaseModel):
    path: str | None = Field(None)
    x: float | None = Field(None)
    y: float | None = Field(None)
    width: int | None = Field(None)
    height: int | None = Field(None)
    person_id: int | None = Field(None)


@router.get("/")
async def getAllFaces():
    faces = await FaceDAO.get_all()
    return JSONResponse({"count": faces.__len__(), "data": [face.to_json() for face in faces]})


@router.get("/{id}")
async def getFaceByID(id: str):
    try:
        faceID = int(id)
        face = await FaceDAO.get(faceID)
        if face:
            return JSONResponse(face.to_json())
        else:
            return JSONResponse(
                status_code=400,
                content={"status": 400, "msg": f"Not found face with ID '{id}'"},
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
async def createFace(face: FaceDTO):
    try:
        params = {
            "FrameFilePath": face.path,
            "X": face.x,
            "Y": face.y,
            "Width": face.width,
            "Height": face.height,
            "person_id": face.person_id,
        }
        print(removeNoneParams(params=params))
        createdFace = await FaceDAO.create(**removeNoneParams(params=params))
        if createdFace:
            print("Face created", createdFace.FrameFilePath)
            print(createdFace.to_json())
            return JSONResponse(status_code=201, content=createdFace.to_json())
    except Exception as e:
        print(e)
        return JSONResponse(status_code=400, content={"status": 400, "msg": e.__str__()})


# @router.put("/{id}")
# async def updatePerson(person: LogDTO,id:str):
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
