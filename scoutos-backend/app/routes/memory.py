from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class MemoryIn(BaseModel):
    user_id: int
    content: str
    topic: str
    tags: List[str] = []

# Temporary in-memory store until database integration
fake_memories: List[dict] = []


@router.post("/add")
def add_memory(mem: MemoryIn):
    """Add a memory entry for a user."""
    fake_memories.append(mem.dict())
    return {"message": "Memory saved!", "memory": mem}


@router.get("/list")
def list_memories(user_id: int = Query(..., description="ID of the user")):
    """Return all memories for the given user."""
    return [m for m in fake_memories if m["user_id"] == user_id]


@router.get("/search")
def search_memories(
    user_id: int,
    topic: Optional[str] = None,
    tag: Optional[str] = None,
):
    """Search memories for a user filtered by topic or tag."""
    result = [m for m in fake_memories if m["user_id"] == user_id]
    if topic:
        result = [m for m in result if m["topic"] == topic]
    if tag:
        result = [m for m in result if tag in m.get("tags", [])]
    return result
