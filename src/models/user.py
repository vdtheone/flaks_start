from sqlalchemy import Column, Integer, String, Boolean
from config import Base, engine


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    is_varified = Column(Boolean, default=False)
    otp = Column(Integer)


# Base.metadata.create_all(engine)
