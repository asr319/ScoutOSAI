from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field
from typing import Any, List, Dict, Generator
from app.models.memory import Memory
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.services.memory_service import MemoryService
from app.services.auth_service import verify_token

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    return verify_token(credentials.credentials)


router = APIRouter(dependencies=[Depends(get_current_user)])


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/status")
def agent_status() -> Dict[str, str]:
    return {"status": "Agent module placeholder"}


class MergeRequest(BaseModel):
    user_id: int
    memory_ids: List[int] = Field(default_factory=list)


def _serialize(mem: Memory) -> Dict[str, Any]:
    return {
        "id": mem.id,
        "user_id": mem.user_id,
        "content": mem.content,
        "topic": mem.topic,
        "tags": mem.tags,
    }


@router.post("/merge")
def merge_memories(
    req: MergeRequest, db: Session = Depends(get_db)
) -> Dict[str, Any]:
    service = MemoryService(db)
    merged = service.merge_memories(req.memory_ids, req.user_id)
    if not merged:
        raise HTTPException(status_code=403, detail="Unauthorized or memories not found")
    return {"memory": _serialize(merged)}
