from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .base import Base
from sqlalchemy.inspection import inspect
import datetime


class Person(Base):
    __tablename__ = "persons"
    id = Column(Integer, primary_key=True)
    name = Column(String)
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
