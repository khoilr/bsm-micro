import base64
import json
import threading
import time
from datetime import datetime
from typing import Awaitable, Callable

import cv2
import socketio
from database.dao.camera import CameraDAO
from database.dao.zone import ZoneDAO
from dotenv import load_dotenv
from fastapi import FastAPI
from loguru import logger
from redis.asyncio import Redis
from services.redis.lifetime import init_redis, shutdown_redis
from web.api.imagelive.socketmanager import SocketManager

load_dotenv()

REDIS_INTERVAL = 2  # seconds
MAX_FRAME_COUNT = 10


class VideoCamera(object):
    def __init__(self, URL):
        self.video = cv2.VideoCapture(URL)
        (self.grabbed, self.frame) = self.video.read()
        self.stop_thread = False
        self.paused = False
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()

    def __del__(self):
        self.stop_thread = True
        self.thread.join()
        self.video.release()
        cv2.destroyAllWindows()

    def get_frame(self):
        with self.lock:
            image = self.frame
            _, jpeg = cv2.imencode(".jpg", image)
            return jpeg.tobytes()

    def update(self):
        while not self.stop_thread:
            with self.lock:
                if self.paused:
                    continue
            time.sleep(0.05)
            (self.grabbed, self.frame) = self.video.read()

    def stop(self):
        with self.lock:
            self.stop_thread = True

    def continue_thread(self):
        with self.lock:
            self.paused = False

    def pause(self):
        with self.lock:
            self.paused = True


def register_startup_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application startup.

    This function uses fastAPI app to store data
    in the state, such as db_engine.

    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("startup")
    async def _startup() -> None:  # noqa: WPS430
        # zone = await ZoneDAO.create(description='blabla')
        # await CameraDAO.create(id=1, name='blabla', description="blabla",connect_uri="rtsp://0.tcp.ap.ngrok.io:10708/user:1cinnovation;pwd:1cinnovation123", type=1, zone=zone)
        app.middleware_stack = None
        // init_redis(app)
        app.middleware_stack = app.build_middleware_stack()
        pass  # noqa: WPS420

    return _startup


def register_shutdown_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application's shutdown.

    :param app: fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("shutdown")
    async def _shutdown() -> None:  # noqa: WPS430
        // await shutdown_redis(app)
        pass  # noqa: WPS420

    return _shutdown


def handleConnectedCLient(camera: VideoCamera, *args, **kwargs):
    try:
        frame = camera.get_frame()
        base64_string = base64.b64encode(frame).decode("utf-8")
        response = {"type": "base64", "data": base64_string}
        return json.dumps(response)
    except:
        return ""


def register_socket_from_app(app: FastAPI):
    """
    Register socket io to app.

    Args:
        app (FastAPI): FastAPI app
    """
    sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=[])
    sio_app = socketio.ASGIApp(socketio_server=sio)
    app.mount("/ws", sio_app)
    CONNECTED_SOCKETS = []
    camera_list = {}

    @sio.event
    async def connect(sid, environ, auth):
        # logger.info("Client connect with id: " + sid)
        CONNECTED_SOCKETS.append(sid)
        await sio.emit("message", "connected successfull with id" + sid)

    @sio.event
    def disconnect(sid):
        # logger.info("disconnect", sid)
        CONNECTED_SOCKETS.remove(sid)

    @sio.on("live_data")
    async def subscribe(sid, data):
        logger.info("Subscribe live data event")
        data = data[0]
        if data not in camera_list:
            cameraID = 1
            try:
                cameraID = int(data)
            except Exception as e:
                print(e)
            camera_model = await CameraDAO.get(camera_id=cameraID)
            print("Camera Model:", camera_model.to_json())
            camera_list[cameraID] = VideoCamera(camera_model.connect_uri)
        prevTime = datetime.now().timestamp()
        redis_pool = app.state.redis_pool
        async with Redis(connection_pool=redis_pool) as redis:
            # if camera data exist then execute
            if camera_list[cameraID]:
                while sid in CONNECTED_SOCKETS:
                    res = handleConnectedCLient(camera_list[cameraID])
                    await sio.send(data=res)
                    try:
                        currentTime = datetime.now().timestamp()
                        if (currentTime - prevTime) >= REDIS_INTERVAL:
                            # update prevtime
                            prevTime = currentTime
                            current_value = await redis.xrange("frames", count=MAX_FRAME_COUNT)
                            # handle data from redis stream
                            streamData = []
                            for data in current_value:
                                sData = {k.decode(): v.decode() for k, v in data[1].items()}
                                streamData.append(sData)
                            respond = {"type": "redis", "data": streamData}
                            # send to client
                            await sio.send(data=json.dumps(respond))
                            # if prev_value != current_value:
                            #     # res = current_value
                            #     res = {
                            #         "type": "redis",
                            #         "data": current_value,
                            #     }
                            #     await sio.send(data=res)
                    except Exception as e:
                        print(e)

        logger.info("Socket with ID " + sid + " close event")
