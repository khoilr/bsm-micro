import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()
postgres_host = os.environ.get("HRM_DB_HOST", "localhost")
postgres_port = os.environ.get("HRM_DB_PORT", "47000")
postgres_user = os.environ.get("HRM_DB_USER", "postgres")
postgres_password = os.environ.get("HRM_DB_PASS", "postgres")
postgres_db_name = os.environ.get("HRM_DB_NAME", "postgres")
DB_URL = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db_name}"

Base = declarative_base()

from src.database.models.employee import Employee
from src.database.models.time import Time

engine = create_engine(DB_URL)
Session = sessionmaker(autoflush=False, bind=engine)

session = Session()
