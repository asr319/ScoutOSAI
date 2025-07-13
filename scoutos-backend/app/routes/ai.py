"""Routes related to AI interactions using the OpenAI API."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import AsyncOpenAI
import os
from typing import Dict, List

router = APIRouter()


class AIRequest(BaseModel):
    prompt: str


async def _ask_openai(prompt: str, max_tokens: int = 200) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY environment variable is not set",
        )

    try:
        client = AsyncOpenAI(api_key=api_key)
        resp = await client.chat.completions.acreate(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=f"OpenAI request failed: {exc}",
        )

    return resp.choices[0].message.content


@router.post("/chat")
async def ai_chat(req: AIRequest) -> Dict[str, str]:
    answer = await _ask_openai(req.prompt)
    return {"response": answer}


class TagRequest(BaseModel):
    content: str


@router.post("/tags")
async def ai_tags(req: TagRequest) -> Dict[str, List[str]]:
    prompt = (
        "Suggest 3 to 5 short single-word tags for the following text. "
        "Return only a comma separated list of the tags.\n" + req.content
    )
    answer = await _ask_openai(prompt)
    tags = [t.strip() for t in answer.split(";") if t.strip()]
    if len(tags) == 1:
        tags = [t.strip() for t in answer.split(",") if t.strip()]
    return {"tags": tags}


class MergeAdviceRequest(BaseModel):
    memory_a: str
    memory_b: str


@router.post("/merge")
async def ai_merge(req: MergeAdviceRequest) -> Dict[str, str]:
    prompt = (
        "Provide guidance on how to merge the following two memory entries and "
        "explain the reasoning:\nMemory A:\n" + req.memory_a + "\nMemory B:\n" + req.memory_b
    )
    answer = await _ask_openai(prompt)
    return {"response": answer}


class SummaryRequest(BaseModel):
    content: str


@router.post("/summary")
async def ai_summary(req: SummaryRequest) -> Dict[str, str]:
    prompt = "Summarize the following text in a short paragraph:\n" + req.content
    answer = await _ask_openai(prompt, max_tokens=100)
    return {"summary": answer}

