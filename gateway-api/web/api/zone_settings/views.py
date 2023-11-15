import fastapi
from database.dao.zone_setting import ZoneSettingDAO
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/zone-settings")


@router.get("/")
async def getAllZoneSetting():
    zone_settings = await ZoneSettingDAO.get_all()
    return JSONResponse(
        {"count": zone_settings.__len__(), "data": [zone_setting.to_json() for zone_setting in zone_settings]}
    )


@router.get("/{id}")
async def getZoneSettingByID(id: str):
    try:
        zoneID = int(id)
        zone_setting = await ZoneSettingDAO.get(zoneID)
        if zone_setting:
            return JSONResponse(zone_setting.to_json())
        else:
            return JSONResponse(
                status_code=400,
                content={"status": 400, "msg": f'Not found zone_setting with ID "{id}"'},
            )
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "status": 400,
                "msg": e.__str__(),
            },
        )


@router.get("/filter")
async def getZoneSettingByID(param: fastapi.Request):
    try:
        param = await param.json()
        zone_settings = await ZoneSettingDAO.filter(param)
        if zone_settings:
            {"count": zone_settings.__len__(), "data": [zone_setting.to_json() for zone_setting in zone_settings]}
        else:
            return JSONResponse(
                status_code=400,
                content={"status": 400, "msg": f'Not found zone_setting with param "{param}"'},
            )
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "status": 400,
                "msg": e.__str__(),
            },
        )
