from src.database import session
from src.database.models.employee import Employee as EmployeeModel


class Employee:
    @staticmethod
    def get_or_create(**kwargs) -> EmployeeModel:
        employee = session.query(EmployeeModel).filter_by(**kwargs).first()
        if employee is None:
            employee = EmployeeModel(**kwargs)
            session.add(employee)
            session.commit()
        return employee
