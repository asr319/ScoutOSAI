from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.memory import Memory
from pydantic import BaseModel, Field
from typing import List, Optional
import datetime

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
    tags: List[str] = Field(default_factory=list)


class MemoryOut(MemoryIn):
    id: int
    timestamp: datetime.datetime

@router.post("/add")
def add_memory(mem: MemoryIn, db: Session = Depends(get_db)):
    db_mem = Memory(
        user_id=mem.user_id,
        content=mem.content,
        topic=mem.topic,
        tags=mem.tags,
        timestamp=datetime.datetime.utcnow(),
    )
    db.add(db_mem)
    db.commit()
    db.refresh(db_mem)
    return db_mem


@router.get("/list", response_model=List[MemoryOut])
def list_memories(user_id: int, db: Session = Depends(get_db)):
    return db.query(Memory).filter(Memory.user_id == user_id).all()


@router.get("/search", response_model=List[MemoryOut])
def search_memories(
    user_id: int,
    topic: Optional[str] = None,
    tag: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Memory).filter(Memory.user_id == user_id)
    if topic:
        query = query.filter(Memory.topic == topic)
    if tag:
        query = query.filter(Memory.tags.contains([tag]))
    return query.all()


@router.delete("/delete/{memory_id}")
def delete_memory(memory_id: int, db: Session = Depends(get_db)):
    mem = db.query(Memory).get(memory_id)
    if not mem:
        raise HTTPException(status_code=404, detail="Memory not found")
    db.delete(mem)
    db.commit()
    return {"detail": "Memory deleted"}
