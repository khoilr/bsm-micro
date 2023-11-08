from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base  # Make sure to import Base from the base module

engine = create_engine('sqlite:///example.db')
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)
