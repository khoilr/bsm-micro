import fastapi
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from database.dao.attendace import AttendanceTrackingDAO

router = APIRouter(prefix="/attendance")


@router.get("/")
async def getAllAttendance():
    attendances = await AttendanceTrackingDAO.get_all()
    return JSONResponse({"count": attendances.__len__(), "data": [attendance.to_json() for attendance in attendances]})


@router.get("/{id}")
async def getAttendanceByID(id: str):
    try:
        attendanceID = int(id)
        attendance = await AttendanceTrackingDAO.get(attendanceID)
        if attendance:
            return JSONResponse(attendance.to_json())
        else:
            return JSONResponse(
                status_code=400,
                content={"status": 400, "msg": f'Not found attendance with ID "{id}"'},
            )
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "status": 400,
                "msg": e.__str__(),
            },
        )
