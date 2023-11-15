from typing import List

from settings import settings

MODELS_MODULES: List[str] = [
    "database.models.dummy_model",
    "database.models.attendance",
    "database.models.camera",
    "database.models.face",
    "database.models.intruderlog",
    "database.models.person",
    "database.models.user",
    "database.models.zone",
    "database.models.event",
    "database.models.event_log",
    "database.models.zone_setting",
]  # noqa: WPS407

TORTOISE_CONFIG = {  # noqa: WPS407
    "connections": {
        "default": str(settings.db_url),
    },
    "apps": {
        "models": {
            "models": MODELS_MODULES + ["aerich.models"],
            "default_connection": "default",
        },
    },
}
