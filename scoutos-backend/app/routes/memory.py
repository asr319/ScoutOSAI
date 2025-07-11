from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class MemoryIn(BaseModel):
    user_id: int
    content: str
    topic: str
    tags: List[str]

@router.post("/add")
def add_memory(mem: MemoryIn):
    # TODO: Store in database
    return {"message": "Memory added", "memory": mem}
