from typing import Dict, Generator
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models.user import User
from app.models.memory import Memory
from app.services.auth_service import verify_token

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    return verify_token(credentials.credentials)


router = APIRouter()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/analytics")
def get_analytics(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)) -> Dict[str, int]:
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    users = db.query(User).count()
    memories = db.query(Memory).count()
    return {"users": users, "memories": memories}
