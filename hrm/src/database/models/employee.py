import sqlalchemy as sa
from src.database import Base


class Employee(Base):
    __tablename__ = "employees"
    id = sa.Column(sa.UUID, primary_key=True, default=sa.func.uuid_generate_v4())
    hrm_id = sa.Column(sa.String, nullable=False, unique=True)
    name = sa.Column(sa.String, nullable=False)
    times = sa.orm.relationship("Time", back_populates="employee")
