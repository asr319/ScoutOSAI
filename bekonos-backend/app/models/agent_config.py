from sqlalchemy import Column, Integer, String, Boolean, JSON
from .base import Base


class AgentConfig(Base):
    __tablename__ = "agent_configs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    enabled = Column(Boolean, default=True)
    settings = Column(JSON, default={})
