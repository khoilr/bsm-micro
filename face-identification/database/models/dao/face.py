from database.models.dto.face import Face
from database import session
from datetime import datetime


class FaceDAO:
    @staticmethod
    def insert_or_get(
        image_url: str,
        drew_image_url: str,
        x: int,
        y: int,
        w: int,
        h: int,
        person_id: str,
        camera_id: str,
        created_at: datetime,
    ) -> Face:
        face = (
            session.query(Face)
            .filter_by(
                image_url=image_url,
                drew_image_url=drew_image_url,
                x=x,
                y=y,
                w=w,
                h=h,
                created_at=created_at,
            )
            .first()
        )

        if face:
            return face
        else:
            new_face = Face(
                x=x,
                y=y,
                w=w,
                h=h,
                image_url=image_url,
                drew_image_url=drew_image_url,
                person_id=person_id,
                camera_id=camera_id,
                created_at=created_at,
            )
            session.add(new_face)
            session.commit()
            return new_face

    @staticmethod
    def get_faces_by_camera_name(camera_name: str) -> list[Face]:
        return session.query(Face).join(Face.camera).filter_by(name=camera_name).all()

    @staticmethod
    def get_all() -> list[Face]:
        return session.query(Face).all()
