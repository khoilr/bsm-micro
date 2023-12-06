from src.database import session
from src.database.models.time import Time as TimeModel
from datetime import datetime
from uuid import UUID


class Time:
    @staticmethod
    def create(**kwargs):
        time = TimeModel(**kwargs)
        session.add(time)
        session.commit()
        return time

    @staticmethod
    def get_latest_in_date(employee_id: UUID, _date: datetime):
        time = (
            session.query(TimeModel)
            .filter(TimeModel.employee_id == employee_id)
            .filter(TimeModel.checkin_at >= _date)
            .order_by(TimeModel.checkin_at.desc())
            .first()
        )
        return time

    @staticmethod
    def update(time: TimeModel, **kwargs):
        for key, value in kwargs.items():
            setattr(time, key, value)
        session.commit()
        return time
