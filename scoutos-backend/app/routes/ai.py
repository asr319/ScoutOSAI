"""Routes related to AI interactions using the OpenAI API."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import AsyncOpenAI
import os

router = APIRouter()


class AIRequest(BaseModel):
    prompt: str

@router.post("/chat")
async def ai_chat(req: AIRequest):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY environment variable is not set",
        )

    client = AsyncOpenAI(api_key=api_key)

    try:
        resp = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": req.prompt}],
            max_tokens=200,
        )
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"OpenAI request failed: {exc}")

    answer = resp.choices[0].message.content
    return {"response": answer}
