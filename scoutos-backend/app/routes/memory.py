from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Any, Dict, Generator, List, Optional
import asyncio

from app.websockets import manager
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.services.memory_service import MemoryService
from app.services.auth_service import verify_token

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Dict[str, Any]:
    return verify_token(credentials.credentials)


router = APIRouter()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class MemoryIn(BaseModel):
    user_id: int
    content: str
    topic: str
    tags: List[str] = Field(default_factory=list)


def _serialize(mem) -> Dict[str, Any]:
    return {
        "id": mem.id,
        "user_id": mem.user_id,
        "content": mem.content,
        "topic": mem.topic,
        "tags": mem.tags,
    }




@router.post("/add")
async def add_memory(
    mem: MemoryIn,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    if mem.user_id != int(current_user["sub"]):
        raise HTTPException(status_code=403, detail="Unauthorized")

    service = MemoryService(db)
    new_mem = service.add_memory(mem.model_dump())
    await manager.send_personal_message(
        {"type": "memory", "action": "added", "memory": _serialize(new_mem)},
        mem.user_id,
    )
    return {"message": "Memory added", "memory": _serialize(new_mem)}


@router.put("/update/{memory_id}")
async def update_memory(
    memory_id: int,
    mem: MemoryIn,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    service = MemoryService(db)
    existing = service.get_memory(memory_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Memory not found")
    if mem.user_id != int(current_user["sub"]):
        raise HTTPException(status_code=403, detail="Unauthorized")
    if existing.user_id != mem.user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    updated = service.update_memory(memory_id, mem.user_id, mem.dict())
    await manager.send_personal_message(
        {"type": "memory", "action": "updated", "memory": _serialize(updated)},
        mem.user_id,
    )
    return {"message": "Memory updated", "memory": _serialize(updated)}


@router.get("/list")
async def list_memories(
    user_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[Dict[str, Any]]:
    if user_id != int(current_user["sub"]):
        raise HTTPException(status_code=403, detail="Unauthorized")

    service = MemoryService(db)
    mems = service.list_memories(user_id)
    return [_serialize(m) for m in mems]


@router.get("/search")
async def search_memories(
    user_id: int,
    topic: Optional[str] = None,
    tag: Optional[str] = None,
    content: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[Dict[str, Any]]:
    if user_id != int(current_user["sub"]):
        raise HTTPException(status_code=403, detail="Unauthorized")

    service = MemoryService(db)
    mems = service.search_memories(user_id, topic=topic, tag=tag, content=content)
    return [_serialize(m) for m in mems]


@router.delete("/delete/{memory_id}")
async def delete_memory(
    memory_id: int,
    user_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Dict[str, str]:
    if user_id != int(current_user["sub"]):
        raise HTTPException(status_code=403, detail="Unauthorized")

    service = MemoryService(db)
    existing = service.get_memory(memory_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Memory not found")
    if existing.user_id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if not service.delete_memory(memory_id, user_id):
        raise HTTPException(status_code=404, detail="Memory not found")
    await manager.send_personal_message(
        {"type": "memory", "action": "deleted", "memory": _serialize(existing)},
        user_id,
    )
    return {"message": "Memory deleted"}
