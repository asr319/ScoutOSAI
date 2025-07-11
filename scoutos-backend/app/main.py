from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import memory, user, agent, ai
from app.db import engine
from app.models.base import Base
from app.models import memory as memory_model, user as user_model

app = FastAPI(title="ScoutOSAI Backend")

# Allow all origins during early development. Limit in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables if they do not exist
Base.metadata.create_all(bind=engine)

app.include_router(memory.router, prefix="/memory")
app.include_router(user.router, prefix="/user")
app.include_router(agent.router, prefix="/agent")
app.include_router(ai.router, prefix="/ai")

@app.get("/")
async def root():
    return {"status": "ScoutOSAI backend running"}
