from dto.face import Face
from database import session


class FaceDAO:
    @staticmethod
    def get(id: str):
        face = session.query(Face).filter_by(id=id).first()
        if face:
            return face
        else:
            return None

    @staticmethod
    def insert_or_create(
        image_url: str,
        drew_image_url: str,
        x: int,
        y: int,
        width: int,
        height: int,
        person_id: str,
        camera_id: str,
    ):
        face = (
            session.query(Face)
            .filter_by(
                image_url=image_url,
                drew_image_url=drew_image_url,
                x=x,
                y=y,
                w=width,
                h=height,
            )
            .first()
        )
        if face:
            return face
        else:
            new_face = Face(
                x=x,
                y=y,
                w=width,
                h=height,
                image_url=image_url,
                drew_image_url=drew_image_url,
                person_id=person_id,
                camera_id=camera_id,
            )
            session.add(new_face)
            session.commit()
            return new_face
