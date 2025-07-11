from fastapi import APIRouter
from pydantic import BaseModel
import openai
import os

router = APIRouter()

openai.api_key = os.getenv("OPENAI_API_KEY")

class AIRequest(BaseModel):
    prompt: str

@router.post("/chat")
async def ai_chat(req: AIRequest):
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": req.prompt}],
        max_tokens=200
    )
    answer = resp.choices[0].message["content"]
    return {"response": answer}
