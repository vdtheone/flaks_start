from sqlalchemy import Column, Integer, String
from config import Base, engine


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)


# Base.metadata.create_all(engine)