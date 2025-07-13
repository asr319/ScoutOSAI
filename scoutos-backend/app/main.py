from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import memory, user, agent, ai
import os


def _get_allowed_origins() -> list[str]:
    """Return allowed CORS origins from environment."""
    origins = os.getenv("ALLOWED_ORIGINS", "*")
    return [origin.strip() for origin in origins.split(",")]

app = FastAPI(title="ScoutOSAI Backend")

# Configure CORS from environment variable
app.add_middleware(
    CORSMiddleware,
    allow_origins=_get_allowed_origins(),
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
