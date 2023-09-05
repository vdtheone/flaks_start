from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

load_dotenv()

db_url = os.environ.get("DATABASE_URL")

engine = create_engine(db_url)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
