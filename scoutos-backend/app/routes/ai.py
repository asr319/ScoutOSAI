"""Routes related to AI interactions using the OpenAI API."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import openai
import os
from typing import Dict

router = APIRouter()


class AIRequest(BaseModel):
    prompt: str


@router.post("/chat")
async def ai_chat(req: AIRequest) -> Dict[str, str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY environment variable is not set",
        )

    openai.api_key = api_key

    try:
        resp = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": req.prompt}],
            max_tokens=200,
        )
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"OpenAI request failed: {exc}")

    answer = resp.choices[0].message.content
    return {"response": answer}
