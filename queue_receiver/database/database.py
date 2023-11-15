from .db_config import Session, init_db
from .models import Face, Person

init_db()

session = Session()
