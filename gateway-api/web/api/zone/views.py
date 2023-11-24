from fastapi import APIRouter
from fastapi.responses import JSONResponse
from loguru import logger
from database.dao.zone import ZoneDAO
from pydantic import BaseModel, Field
from server.web.api.utils import removeNoneParams

router = APIRouter(prefix="/zone")


class ZoneBaseDTO(BaseModel):
    # name: str | None = Field(None)
    description: str | None = Field(None)
    placeholder_url: str | None = Field(None)


class ZoneCreateDTO(ZoneBaseDTO):
    name: str | None = Field(..., description="This field must not be empty")


class ZoneUpdateDTO(ZoneBaseDTO):
    name: str | None = Field(None)


@router.get("/")
async def getAllZone():
    zones = await ZoneDAO.get_all()
    return JSONResponse(
        {"count": zones.__len__(), "data": [zone.to_json() for zone in zones]}
    )


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


@router.post("/")
async def createZone(zone: ZoneCreateDTO):
    try:
        params = {
            "name": zone.name,
            "description": zone.description,
            "placeholder_url": zone.placeholder_url,
        }
        createdZone = await ZoneDAO.create(**removeNoneParams(params=params))

        if createdZone:
            return JSONResponse(status_code=201, content=createdZone.to_json())
    except Exception as e:
        logger.error(e)
        return JSONResponse(
            status_code=400, content={"status": 400, "msg": e.__str__()}
        )


@router.put("/{id}")
async def updateZone(zone: ZoneUpdateDTO, id: str):
    try:
        zoneID = int(id)
        params = {
            "name": zone.name,
            "description": zone.description,
            "placeholder_url": zone.placeholder_url,
        }
        print(removeNoneParams(params=params))
        updatedZone = await ZoneDAO.update(zone_id=zoneID, **removeNoneParams(params))
        if updatedZone:
            return JSONResponse(status_code=200, content=updatedZone.to_json())
        else:
            raise Exception("Not found zone to update")
    except Exception as e:
        return JSONResponse(
            status_code=400, content={"status": 400, "msg": e.__str__()}
        )


@router.delete("/{id}")
async def deleteZoneByID(id: str):
    try:
        zoneID = int(id)
        deletedZone = await ZoneDAO.delete(zone_id=zoneID)

        if deletedZone:
            return JSONResponse(
                status_code=200,
                content={
                    "status": 200,
                    "msg": f"Delete zone with ID '{id}' succesfully",
                },
            )
        else:
            return JSONResponse(
                status_code=200,
                content={"status": 200, "msg": "Not found zone to delete"},
            )
    except Exception as e:
        return JSONResponse(
            status_code=400, content={"status": 400, "msg": e.__str__()}
        )
