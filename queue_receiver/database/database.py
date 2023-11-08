from db_config import init_db, Session
from models import Person, Face  # Importing the models

# Initialize the database
init_db()

# Create a new session
session = Session()

# Add and commit new objects
new_person = Person(name='John Doe')
session.add(new_person)

new_face = Face(frame_file_path='path/to/image.jpg', x=120.0, y=75.5, width=100, height=150)
session.add(new_face)

session.commit()

# Query and print objects
person = session.query(Person).first()
print(f'Person: {person.name}, Created at: {person.created_at}, Updated at: {person.updated_at}')

face = session.query(Face).first()
print(f'Face ID: {face.id}, Frame File Path: {face.frame_file_path}')