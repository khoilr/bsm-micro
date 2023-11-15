import fastapi
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from database.dao.action import ActionDAO

router = APIRouter(prefix="/action")


@router.get("/")
async def getAllAction():
    actions = await ActionDAO.get_all()
    return JSONResponse({"count": actions.__len__(), "data": [action.to_json() for action in actions]})


@router.get("/{id}")
async def getActionByID(id: str):
    try:
        actionID = int(id)
        action = await ActionDAO.get(actionID)
        if action:
            return JSONResponse(action.to_json())
        else:
            return JSONResponse(
                status_code=400,
                content={"status": 400, "msg": f'Not found action with ID "{id}"'},
            )
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "status": 400,
                "msg": e.__str__(),
            },
        )
