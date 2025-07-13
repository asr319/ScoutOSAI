from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import openai
import os
from typing import Dict

router = APIRouter()

openai.api_key = os.getenv("OPENAI_API_KEY")


class AIRequest(BaseModel):
    prompt: str


@router.post("/chat")
async def ai_chat(req: AIRequest) -> Dict[str, str]:
    if not openai.api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY environment variable is not set"
        )

    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": req.prompt}],
        max_tokens=200,
    )
    answer = resp.choices[0].message["content"]
    return {"response": answer}
