from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import memory, user, agent, ai
import os

app = FastAPI(title="ScoutOSAI Backend")

# Configure CORS
origins_env = os.getenv("ALLOWED_ORIGINS")
allowed_origins: list[str]

if origins_env:
    allowed_origins = [origin.strip() for origin in origins_env.split(",") if origin.strip()]
else:
    allowed_origins = ["http://localhost:5173", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(memory.router, prefix="/memory")
app.include_router(user.router, prefix="/user")
app.include_router(agent.router, prefix="/agent")
app.include_router(ai.router, prefix="/ai")


@app.get("/")
async def root() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ScoutOSAI backend running"}
