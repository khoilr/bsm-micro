from models.dto.camera import Camera
from database import session


class CameraDAO:
    @staticmethod
    def get(id: str):
        camera = session.query(Camera).filter_by(id=id).first()
        if camera:
            return camera
        else:
            return None

    @staticmethod
    def insert_or_create(name: str):
        camera = session.query(Camera).filter_by(name=name).first()
        if camera:
            return camera
        else:
            new_camera = Camera(name=name)
            session.add(new_camera)
            session.commit()
            return new_camera
