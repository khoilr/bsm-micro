from fastapi.routing import APIRouter

from web.api import (action, attendance, authentication, camera, event, face,
                     imagelive, intruder_log, log, people, zone,
                     zone_settings)

api_router = APIRouter()
api_router.include_router(authentication.router)
api_router.include_router(people.router)
api_router.include_router(zone.router)
api_router.include_router(event.router)
api_router.include_router(imagelive.router)
api_router.include_router(camera.router)
api_router.include_router(log.router)
api_router.include_router(face.router)
api_router.include_router(action.router)
api_router.include_router(attendance.router)
api_router.include_router(intruder_log.router)
api_router.include_router(zone_settings.router)
