from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from src.database import Base


class Camera(Base):
    __tablename__ = "cameras"

    # Attributes
    id = sa.Column(sa.UUID, primary_key=True, default=uuid4)
    name = sa.Column(sa.String(255), nullable=False)
    created_at = sa.Column(sa.DateTime, nullable=False, server_default=sa.func.now())
    updated_at = sa.Column(
        sa.DateTime,
        nullable=False,
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
    )

    """Relationships"""
    # A camera has many faces
    faces = relationship(
        "Face",
        back_populates="camera",
        cascade="all, delete",
    )
