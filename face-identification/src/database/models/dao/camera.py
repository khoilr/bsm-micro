from src.database.models.dto.camera import Camera
from src.database import session


class CameraDAO:
    @staticmethod
    def insert_or_get(name: str) -> Camera:
        camera = session.query(Camera).filter_by(name=name).first()
        if camera:
            return camera
        else:
            new_camera = Camera(name=name)
            session.add(new_camera)
            session.commit()
            return new_camera
