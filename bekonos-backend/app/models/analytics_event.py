from __future__ import annotations

import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON

from .base import Base


class AnalyticsEvent(Base):
    """Record of an application event for analytics."""

    __tablename__ = "analytics_events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    event_type = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    payload = Column(JSON)
