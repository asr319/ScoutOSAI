"""Routes related to AI interactions using the OpenAI API."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from openai import AsyncOpenAI
import os
from typing import Dict, Generator, List
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


class AIRequest(BaseModel):
    prompt: str


@router.post("/chat")
async def ai_chat(req: AIRequest) -> Dict[str, str]:
    service = AgentService()
    answer = await service.chat(req.prompt)
    return {"response": answer}


class TagRequest(BaseModel):
    text: str


@router.post("/tags")
async def ai_tags(req: TagRequest) -> Dict[str, List[str]]:
    prompt = (
        "Suggest 3 to 5 short single-word tags for the following text. "
        "Return only a comma separated list of the tags.\n" + req.text
    )
    answer = await _ask_openai(prompt)
    tags = [t.strip() for t in answer.split(";") if t.strip()]
    if len(tags) == 1:
        tags = [t.strip() for t in answer.split(",") if t.strip()]
    service = AgentService()
    tags = await service.generate_tags(req.content)
    return {"tags": tags}


class MergeRequest(BaseModel):
    memory_ids: List[int]


@router.post("/merge")
async def ai_merge(
    req: MergeRequest, db: Session = Depends(get_db)
) -> Dict[str, str]:
    service = MemoryService(db)
    memories: List[str] = []
    for mem_id in req.memory_ids:
        mem = service.get_memory(mem_id)
        if not mem:
            raise HTTPException(status_code=404, detail="Memory not found")
        memories.append(mem.content)

    joined = "\n".join(
        f"Memory {i + 1}:\n{content}" for i, content in enumerate(memories)
    )
    prompt = (
        "Should these memories be merged? Reply 'Yes' or 'No' and include a brief "
        "reason.\n" + joined
    )
    answer = await _ask_openai(prompt)
    return {"verdict": answer}
async def ai_merge(req: MergeAdviceRequest) -> Dict[str, str]:
    service = AgentService()
    answer = await service.merge_advice(req.memory_a, req.memory_b)
    return {"response": answer}


class SummaryRequest(BaseModel):
    content: str


@router.post("/summary")
async def ai_summary(req: SummaryRequest) -> Dict[str, str]:
    service = AgentService()
    prompt = "Summarize the following text in a short paragraph:\n" + req.content
    answer = await service.chat(prompt, max_tokens=100)
    return {"summary": answer}

