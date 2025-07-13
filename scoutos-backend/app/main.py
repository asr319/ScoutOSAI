from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import memory, user, agent, ai
import os

app = FastAPI(title="ScoutOSAI Backend")

# Read allowed CORS origins from the environment. Comma separated values
# are converted into a list. Defaults to "*" for local development.
origins_env: str | None = os.getenv("ALLOWED_ORIGINS")
allowed_origins: list[str] = (
    [o.strip() for o in origins_env.split(",") if o.strip()]
    if origins_env
    else ["*"]
)

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
