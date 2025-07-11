from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class Memory(Base):
    __tablename__ = "memories"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String)
    topic = Column(String)
    tags = Column(JSON)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
