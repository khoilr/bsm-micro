from ..database import Session
from ..models import Face


class FaceDAO:
    @staticmethod
    def get_all():
        with Session() as session:
            return session.query(Face).all()

    @staticmethod
    def get_face_by_id(face_id):
        with Session() as session:
            return session.query(Face).filter(Face.id == face_id).first()

    @staticmethod
    def create_face(frame_file_path, x, y, width, height):
        with Session() as session:
            new_face = Face(frame_file_path=frame_file_path, x=x, y=y, width=width, height=height)
            session.add(new_face)
            session.commit()
            return new_face.to_json()

    @staticmethod
    def update_face(face_id, **kwargs):
        with Session() as session:
            face = session.query(Face).filter(Face.id == face_id).first()
            if face:
                for key, value in kwargs.items():
                    if value is not None and hasattr(face, key):
                        setattr(face, key, value)
                session.commit()
            return face

    @staticmethod
    def delete_face(face_id):
        with Session() as session:
            face = session.query(Face).filter(Face.id == face_id).first()
            if face:
                session.delete(face)
                session.commit()
            return face
