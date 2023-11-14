from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from database import Base


class Person(Base):
    __tablename__ = "persons"

    # Attributes
    id = sa.Column(sa.UUID, primary_key=True, default=uuid4)
    name = sa.Column(sa.String, nullable=False)
    is_known = sa.Column(sa.Boolean, nullable=False, default=False)
    created_at = sa.Column(sa.DateTime, nullable=False, server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())

    """Relationships"""
    # A persons can have many faces
    faces = relationship(
        "Face",
        back_populates="person",
        cascade="all, delete",
    )
