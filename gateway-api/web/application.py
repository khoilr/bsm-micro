import asyncio
from importlib import metadata

import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import UJSONResponse
from tortoise.contrib.fastapi import register_tortoise

from database.config import TORTOISE_CONFIG
from database.dao.user import UserDAO
from web.api.router import api_router
from web.lifetime import (handleConnectedCLient, register_shutdown_event,
                          register_socket_from_app, register_startup_event)


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="bsm_server",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)
    register_socket_from_app(app)
    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")

    # Configures tortoise orm.
    register_tortoise(
        app,
        config=TORTOISE_CONFIG,
        add_exception_handlers=True,
    )

    return app
