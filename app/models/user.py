from sqlalchemy import Column, Integer, String

from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(155))
    email = Column(String(255), unique=True)
