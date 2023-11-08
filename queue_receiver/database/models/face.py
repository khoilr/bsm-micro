from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .base import Base
from sqlalchemy.inspection import inspect
import datetime


class Face(Base):
    __tablename__ = "faces"
    id = Column(Integer, primary_key=True)
    frame_file_path = Column(String)
    x = Column(Float)
    y = Column(Float)
    width = Column(Integer)
    height = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def to_json(self):
        fields = {
            c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs
        }
        for field, value in fields.items():
            if isinstance(value, datetime.datetime):
                fields[field] = value.isoformat()
        return fields
