from sqlalchemy import Column, Integer, ForeignKey, JSON
from .base import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    preferences = Column(JSON, default={})
