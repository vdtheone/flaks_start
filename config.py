import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

db_url = os.environ.get("DATABASE_URL")

engine = create_engine(db_url)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
