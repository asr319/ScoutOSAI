from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List
import openai
import os

router = APIRouter()

fake_memories = []  # Replace with real DB in production


openai.api_key = os.getenv("OPENAI_API_KEY")
>>>>>>> origin/main
class MemoryIn(BaseModel):
    user_id: int
    content: str
    topic: str
    tags: List[str] = []

# Temporary in-memory store until database integration
fake_memories: List[dict] = []


@router.post("/add")
def add_memory(mem: MemoryIn):
<<<<<<< HEAD
    memory_entry = {
        "id": len(fake_memories) + 1,
        "user_id": mem.user_id,
        "content": mem.content,
        "topic": mem.topic,
        "tags": mem.tags,
    }
    fake_memories.append(memory_entry)
    return {"message": "Memory added", "memory": memory_entry}

@router.get("/list/{user_id}")
def list_memories(user_id: int):
    user_mems = [m for m in fake_memories if m["user_id"] == user_id]
    return {"memories": user_mems}

