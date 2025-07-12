from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.services.memory_service import MemoryService

router = APIRouter()


def get_db():
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


def _serialize(mem):
    return {
        "id": mem.id,
        "user_id": mem.user_id,
        "content": mem.content,
        "topic": mem.topic,
        "tags": mem.tags,
    }


@router.post("/add")
def add_memory(mem: MemoryIn, db: Session = Depends(get_db)):
    service = MemoryService(db)
    new_mem = service.add_memory(mem.model_dump())
    return {"message": "Memory added", "memory": _serialize(new_mem)}


@router.put("/update/{memory_id}")
def update_memory(memory_id: int, mem: MemoryIn, db: Session = Depends(get_db)):
    service = MemoryService(db)
    updated = service.update_memory(memory_id, mem.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Memory not found")
    return {"message": "Memory updated", "memory": _serialize(updated)}


@router.get("/list")
def list_memories(user_id: int, db: Session = Depends(get_db)):
    service = MemoryService(db)
    mems = service.list_memories(user_id)
    return [_serialize(m) for m in mems]


@router.get("/search")
def search_memories(
    user_id: int,
    topic: Optional[str] = None,
    tag: Optional[str] = None,
    db: Session = Depends(get_db),
):
    service = MemoryService(db)
    mems = service.search_memories(user_id, topic=topic, tag=tag)
    return [_serialize(m) for m in mems]


@router.delete("/delete/{memory_id}")
def delete_memory(memory_id: int, db: Session = Depends(get_db)):
    service = MemoryService(db)
    if not service.delete_memory(memory_id):
        raise HTTPException(status_code=404, detail="Memory not found")
    return {"message": "Memory deleted"}
