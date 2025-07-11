from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List
from app.db import SessionLocal
from app.services.memory_service import MemoryService

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/status")
def agent_status():
    return {"status": "Agent module placeholder"}


class MergeRequest(BaseModel):
    user_id: int
    memory_ids: List[int] = Field(default_factory=list)


@router.post("/merge")
def merge_memories(req: MergeRequest, db=Depends(get_db)):
    service = MemoryService(db)
    merged = service.merge_memories(req.memory_ids, req.user_id)
    if not merged:
        raise HTTPException(status_code=404, detail="Memories not found")
    return {"memory": merged}
