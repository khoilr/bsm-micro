from src.database import Base
import sqlalchemy as sa


class Time(Base):
    __tablename__ = "times"
    id = sa.Column(sa.String(255), primary_key=True)
    employee_id = sa.Column(sa.UUID, sa.ForeignKey("employees.id"), nullable=False)
    employee = sa.orm.relationship("Employee", back_populates="times")
    checkin_at = sa.Column(sa.DateTime, nullable=False)
    checkout_at = sa.Column(sa.DateTime, nullable=True)
    completed = sa.Column(sa.Boolean, nullable=False, default=False)
    checkin_img = sa.Column(sa.String, nullable=True)
    checkout_img = sa.Column(sa.String, nullable=True)

    def to_dict(self):
        return (
            {
                "id": self.id,
                "employee_id": str(self.employee_id),
                "employee_name": self.employee.name,
                "checkin_at": self.checkin_at.timestamp(),
                "checkout_at": self.checkout_at.timestamp(),
                "completed": self.completed,
                "checkin_img": self.checkin_img,
                "checkout_img": self.checkout_img,
            }
            if self.completed
            else {
                "id": self.id,
                "employee_id": str(self.employee_id),
                "employee_name": self.employee.name,
                "checkin_at": self.checkin_at.timestamp(),
                "checkout_at": 0,
                "completed": self.completed,
                "checkin_img": self.checkin_img,
                "checkout_img": "",
            }
        )
