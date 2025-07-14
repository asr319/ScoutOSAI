from __future__ import annotations

import datetime
from typing import List, Dict, Optional

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.analytics_event import AnalyticsEvent


class AnalyticsService:
    """Service layer for recording and fetching analytics events."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def record_event(
        self, user_id: Optional[int], event_type: str, payload: Dict[str, object]
    ) -> AnalyticsEvent:
        event = AnalyticsEvent(
            user_id=user_id,
            event_type=event_type,
            timestamp=datetime.datetime.utcnow(),
            payload=payload,
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    def get_events(self, user_id: int, limit: int = 100) -> List[AnalyticsEvent]:
        return (
            self.db.query(AnalyticsEvent)
            .filter(AnalyticsEvent.user_id == user_id)
            .order_by(AnalyticsEvent.timestamp.desc())
            .limit(limit)
            .all()
        )

    def summary(self, user_id: int) -> Dict[str, int]:
        rows = (
            self.db.query(AnalyticsEvent.event_type, func.count().label("count"))
            .filter(AnalyticsEvent.user_id == user_id)
            .group_by(AnalyticsEvent.event_type)
            .all()
        )
        return {r.event_type: r.count for r in rows}
