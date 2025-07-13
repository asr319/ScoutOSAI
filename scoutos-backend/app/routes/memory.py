from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Generator
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.services.memory_service import MemoryService

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
    tags: List[str] = []


def _serialize(mem) -> Dict[str, object]:
    return {
        "id": mem.id,
        "user_id": mem.user_id,
        "content": mem.content,
        "topic": mem.topic,
        "tags": mem.tags,
    }


@router.post("/add")
def add_memory(mem: MemoryIn, db: Session = Depends(get_db)) -> Dict[str, object]:
    service = MemoryService(db)
    new_mem = service.add_memory(mem.dict())
    return {"message": "Memory added", "memory": _serialize(new_mem)}


@router.put("/update/{memory_id}")
def update_memory(memory_id: int, mem: MemoryIn, db: Session = Depends(get_db)) -> Dict[str, object]:
    service = MemoryService(db)
    updated = service.update_memory(memory_id, mem.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Memory not found")
    return {"message": "Memory updated", "memory": _serialize(updated)}


@router.get("/list")
def list_memories(user_id: int, db: Session = Depends(get_db)) -> List[Dict[str, object]]:
    service = MemoryService(db)
    mems = service.list_memories(user_id)
    return [_serialize(m) for m in mems]


@router.get("/search")
def search_memories(
    user_id: int,
    topic: Optional[str] = None,
    tag: Optional[str] = None,
    db: Session = Depends(get_db),
) -> List[Dict[str, object]]:
    service = MemoryService(db)
    mems = service.list_memories(user_id)
    if topic:
        mems = [m for m in mems if m.topic == topic]
    if tag:
        mems = [m for m in mems if m.tags and tag in m.tags]
    return [_serialize(m) for m in mems]


@router.delete("/delete/{memory_id}")
def delete_memory(memory_id: int, db: Session = Depends(get_db)) -> Dict[str, str]:
    service = MemoryService(db)
    if not service.delete_memory(memory_id):
        raise HTTPException(status_code=404, detail="Memory not found")
    return {"message": "Memory deleted"}
