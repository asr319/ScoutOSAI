"""Routes related to AI interactions using the OpenAI API."""

from fastapi import APIRouter, Depends, HTTPException
import asyncio
from pydantic import BaseModel
from openai import AsyncOpenAI
import os
from typing import Dict, Generator, List
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.services.memory_service import MemoryService
from app.services.agent_service import AgentService
from app.websockets import manager
from app.services.analytics_service import AnalyticsService
from app.services.agent_service import AgentService

router = APIRouter()


def _notify(event: str, payload: Dict[str, str]) -> None:
    asyncio.create_task(manager.broadcast({"type": "agent", "event": event, **payload}))


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def _ask_openai(prompt: str, max_tokens: int = 200) -> str:
    """Helper for direct OpenAI calls used in certain routes."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY environment variable is not set",
        )
    client = AsyncOpenAI(api_key=api_key)
    completions = client.chat.completions
    if hasattr(completions, "create"):
        resp = await completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )
    else:
        resp = await completions.acreate(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )
    return resp.choices[0].message.content


class AIRequest(BaseModel):
    prompt: str


@router.post("/chat")
async def ai_chat(req: AIRequest, db: Session = Depends(get_db)) -> Dict[str, str]:
    service = AgentService()
    answer = await service.chat(req.prompt)
    _notify("chat", {"response": answer})
    AnalyticsService(db).record_event(None, "ai_chat", {"prompt": req.prompt})
    return {"response": answer}


class TagRequest(BaseModel):
    text: str


@router.post("/tags")
async def ai_tags(
    req: TagRequest, db: Session = Depends(get_db)
) -> Dict[str, List[str]]:
    service = AgentService()
    tags = await service.generate_tags(req.text)
    _notify("tags", {"detail": ",".join(tags)})
    AnalyticsService(db).record_event(None, "ai_tags", {"text": req.text})
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

    if len(memories) < 2:
        raise HTTPException(status_code=400, detail="At least two memories required")

    agent = AgentService()
    answer = await agent.merge_advice(memories[0], "\n".join(memories[1:]))
    _notify("merge", {"verdict": answer})
    AnalyticsService(db).record_event(None, "ai_merge", {"ids": req.memory_ids})
    return {"verdict": answer}


class SummaryRequest(BaseModel):
    content: str


@router.post("/summary")
async def ai_summary(
    req: SummaryRequest, db: Session = Depends(get_db)
) -> Dict[str, str]:
    service = AgentService()
    prompt = "Summarize the following text in a short paragraph:\n" + req.content
    answer = await service.chat(prompt, max_tokens=100)
    _notify("summary", {"summary": answer})
    AnalyticsService(db).record_event(None, "ai_summary", {})
    return {"summary": answer}

