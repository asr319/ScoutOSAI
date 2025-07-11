from fastapi import FastAPI
from app.routes import memory, user, agent, ai

app = FastAPI(title="ScoutOSAI Backend")

app.include_router(memory.router, prefix="/memory")
app.include_router(user.router, prefix="/user")
app.include_router(agent.router, prefix="/agent")
app.include_router(ai.router, prefix="/ai")

@app.get("/")
async def root():
    return {"status": "ScoutOSAI backend running"}
