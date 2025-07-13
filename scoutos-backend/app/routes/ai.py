"""Routes related to AI interactions using the OpenAI API."""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, List

from app.services.agent_service import AgentService

router = APIRouter()


class AIRequest(BaseModel):
    prompt: str


@router.post("/chat")
async def ai_chat(req: AIRequest) -> Dict[str, str]:
    service = AgentService()
    answer = await service.chat(req.prompt)
    return {"response": answer}


class TagRequest(BaseModel):
    content: str


@router.post("/tags")
async def ai_tags(req: TagRequest) -> Dict[str, List[str]]:
    service = AgentService()
    tags = await service.generate_tags(req.content)
    return {"tags": tags}


class MergeAdviceRequest(BaseModel):
    memory_a: str
    memory_b: str


@router.post("/merge")
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

