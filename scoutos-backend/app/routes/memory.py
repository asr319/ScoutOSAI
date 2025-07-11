from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List
import openai
import os

router = APIRouter()

openai.api_key = os.getenv("OPENAI_API_KEY")
class MemoryIn(BaseModel):
    user_id: int
    content: str
    topic: str
    tags: List[str] = []

# Temporary in-memory store until database integration
fake_memories: List[dict] = []


@router.post("/add")
def add_memory(mem: MemoryIn):
    # TODO: Store in database
    if not mem.tags:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Suggest 3 tags for this memory: {mem.content}"}],
            max_tokens=30
        )
        tags = [t.strip() for t in resp.choices[0].message["content"].split(',')]
    else:
        tags = mem.tags

    return {"message": "Memory added", "memory": {**mem.dict(), "tags": tags}}
