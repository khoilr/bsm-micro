from ..models import Person
from ..database import Session

class PersonDAO:
    
    @staticmethod
    def get_all():
        with Session() as session:
            return session.query(Person).all()

    @staticmethod
    def get_person_by_id(person_id):
        with Session() as session:
            return session.query(Person).filter(Person.id == person_id).first()

    @staticmethod
    def create_person(name):
        with Session() as session:
            new_person = Person(name=name)
            session.add(new_person)
            session.commit()
            return new_person.to_json()

    @staticmethod
    def update_person(person_id, **kwargs):
        with Session() as session:
            person = session.query(Person).filter(Person.id == person_id).first()
            if person:
                for key, value in kwargs.items():
                    if value is not None and hasattr(person, key):
                        setattr(person, key, value)
                session.commit()
            return person


    @staticmethod
    def delete_person(person_id):
        with Session() as session:
            person = session.query(Person).filter(Person.id == person_id).first()
            if person:
                session.delete(person)
                session.commit()
            return person
        
    
