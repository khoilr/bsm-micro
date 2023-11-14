from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///file_name_storage.db")
Session = sessionmaker(bind=engine)
session = Session()
