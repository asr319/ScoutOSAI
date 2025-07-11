from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.routes import memory, user, agent, ai
from app.db import engine
from app.models.base import Base
from app.models import memory as memory_model, user as user_model

app = FastAPI(title="ScoutOSAI Backend")

# Allow all origins during early development. Limit in production.
origins_env = os.getenv("ALLOWED_ORIGINS")
if origins_env:
    allowed_origins = [o.strip() for o in origins_env.split(',') if o.strip()]
else:
    allowed_origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
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
