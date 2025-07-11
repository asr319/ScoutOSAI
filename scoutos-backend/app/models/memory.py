from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from .base import Base
import datetime
from .base import Base


class Memory(Base):
    __tablename__ = "memories"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String)
    topic = Column(String)
    tags = Column(JSON)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
