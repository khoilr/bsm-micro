from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from database import Base


class Face(Base):
    __tablename__ = "faces"

    # Attributes
    id = sa.Column(sa.UUID, primary_key=True, default=uuid4)
    x = sa.Column(sa.Integer, nullable=False)
    y = sa.Column(sa.Integer, nullable=False)
    w = sa.Column(sa.Integer, nullable=False)
    y = sa.Column(sa.Integer, nullable=False)
    created_at = sa.Column(sa.DateTime, nullable=False, server_default=sa.func.now())
    image_url = sa.Column(sa.String(255), nullable=False)
    drawed_image_url = sa.Column(sa.String(255), nullable=False)

    """Relationships"""
    # A face belongs to a person
    person_id = sa.Column(sa.UUID, sa.ForeignKey("persons.id"))
    person = relationship("Person", back_populates="faces")

    # A face belongs to a camera
    camera_id = sa.Column(sa.UUID, sa.ForeignKey("cameras.id"))
    camera = relationship("Camera", back_populates="faces")
