from __future__ import annotations

import csv
import io
from typing import Any, Dict, Generator, List

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models.memory import Memory
from app.models.user import User
from app.services.analytics_service import AnalyticsService
from app.services.auth_service import verify_token

security = HTTPBearer()
router = APIRouter()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Dict[str, Any]:
    return verify_token(credentials.credentials)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/events")
def list_events(
    limit: int = 100,
    format: str = "json",
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = AnalyticsService(db)
    events = service.get_events(int(current_user["sub"]), limit=limit)
    data = [
        {
            "id": e.id,
            "user_id": e.user_id,
            "event_type": e.event_type,
            "timestamp": e.timestamp.isoformat(),
            "payload": e.payload,
        }
        for e in events
    ]
    if format == "csv":
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys()) if data else csv.DictWriter(
            output, fieldnames=["id", "user_id", "event_type", "timestamp", "payload"]
        )
        writer.writeheader()
        if data:
            writer.writerows(data)
        return Response(content=output.getvalue(), media_type="text/csv")
    return data


@router.get("/summary")
def summary(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Dict[str, int]:
    service = AnalyticsService(db)
    return service.summary(int(current_user["sub"]))


@router.get("/analytics")
def get_analytics(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)) -> Dict[str, int]:
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    users = db.query(User).count()
    memories = db.query(Memory).count()
    return {"users": users, "memories": memories}
