from sqlalchemy import Column, Integer, String
from .base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    role = Column(String, default="user")
    totp_secret = Column(String, nullable=True)
