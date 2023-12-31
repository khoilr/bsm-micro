import datetime

from database import session
from sqlalchemy import Column, Integer, String
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Storage(Base):
    __tablename__ = "storage"
    stored_name = Column(String, primary_key=True)
    original_name = Column(String)
    created_at = Column(String)
    file_size = Column(Integer)

    def to_json(self):
        fields = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        for field, value in fields.items():
            if isinstance(value, datetime.datetime):
                fields[field] = value.isoformat()
        return fields


class StorageDAO:
    @staticmethod
    def get(stored_name):
        storage_object = session.query(Storage).filter_by(stored_name=stored_name).first()
        if storage_object:
            # Change object to json so it's like a line in the old json file
            storage_object = storage_object.to_json()
            return storage_object
        else:
            return None

    @staticmethod
    def delete(stored_name):
        obj_to_delete = session.query(Storage).filter_by(stored_name=stored_name).first()
        if obj_to_delete:
            session.delete(obj_to_delete)
            session.commit()
            return True
        else:
            return False

    @staticmethod
    def create(original_name: str, stored_name: str, created_at: str, file_size: int):
        new_storage = Storage(
            original_name=original_name,
            stored_name=stored_name,
            created_at=created_at,
            file_size=file_size,
        )
        session.add(new_storage)
        session.commit()
        return new_storage
