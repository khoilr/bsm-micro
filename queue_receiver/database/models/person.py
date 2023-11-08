from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .base import Base  # Assuming you've created a base module

class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
