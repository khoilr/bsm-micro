from .db_config import init_db, Session
from .models import Person, Face

init_db()

session = Session()


