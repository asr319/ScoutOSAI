# bekonOS (c) 2025 asr319. All rights reserved. Proprietary.
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import memory, user, agent, ai, analytics
from app.routes import ws, chain
import os


def _get_allowed_origins() -> list[str]:
    """Return allowed CORS origins from environment."""
    origins = os.getenv("ALLOWED_ORIGINS")
    if not origins:
        return ["http://localhost:5173", "http://localhost:3000"]
    return [origin.strip() for origin in origins.split(",") if origin.strip()]


app = FastAPI(title="bekonOS Backend")

# Configure CORS
allowed_origins = _get_allowed_origins()

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
app.include_router(chain.router, prefix="/chain")
app.include_router(analytics.router, prefix="/analytics")
app.include_router(analytics.router, prefix="")
app.include_router(ws.router)


@app.get("/")
async def root() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "bekonOS backend running"}
