from fastapi import FastAPI
from app.routes import memory, user, agent
from app.db import engine
from app.models.memory import Base as MemoryBase
from app.models.user import Base as UserBase

app = FastAPI(title="ScoutOSAI Backend")

# Create tables if they do not exist
MemoryBase.metadata.create_all(bind=engine)
UserBase.metadata.create_all(bind=engine)

app.include_router(memory.router, prefix="/memory")
app.include_router(user.router, prefix="/user")
app.include_router(agent.router, prefix="/agent")

@app.get("/")
async def root():
    return {"status": "ScoutOSAI backend running"}
