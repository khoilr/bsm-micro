from models.dto.person import Person
from database import session    


class PersonDAO:
    @staticmethod
    def get(id: str):
        person = session.query(Person).filter_by(id=id).first()
        if person:
            return person
        else:
            return None

    @staticmethod
    def insert_or_create(name: str):
        person = session.query(Person).filter_by(name=name).first()
        if person:
            return person
        else:
            new_person = Person(name=name)
            session.add(new_person)
            session.commit()
            return new_person