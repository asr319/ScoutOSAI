from sqlalchemy import Column, Integer, String, JSON
from .base import Base


class Chain(Base):
    __tablename__ = "chains"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    actions = Column(JSON, nullable=False)
