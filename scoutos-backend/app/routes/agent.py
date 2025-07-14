from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field
from typing import Any, List, Dict, Generator
from app.models.memory import Memory
from app.models.agent_config import AgentConfig
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.services.memory_service import MemoryService
from app.services.auth_service import verify_token

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    return verify_token(credentials.credentials)


router = APIRouter()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/status")
def agent_status(current_user: dict = Depends(get_current_user)) -> Dict[str, str]:
    return {"status": "Agent module placeholder"}


class MergeRequest(BaseModel):
    user_id: int
    memory_ids: List[int] = Field(default_factory=list)


def _serialize(mem: Memory) -> Dict[str, Any]:
    return {
        "id": mem.id,
        "user_id": mem.user_id,
        "content": mem.content,
        "topic": mem.topic,
        "tags": mem.tags,
    }


@router.post("/merge")
def merge_memories(
    req: MergeRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    if req.user_id != int(current_user["sub"]):
        raise HTTPException(status_code=403, detail="Unauthorized")

    service = MemoryService(db)
    merged = service.merge_memories(req.memory_ids, req.user_id)
    if not merged:
        raise HTTPException(status_code=403, detail="Unauthorized or memories not found")
    return {"memory": _serialize(merged)}


class AgentConfigRequest(BaseModel):
    name: str
    enabled: bool = True
    settings: Dict[str, Any] = Field(default_factory=dict)


@router.get("/config")
def list_configs(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    configs = db.query(AgentConfig).all()
    return [
        {"name": c.name, "enabled": c.enabled, "settings": c.settings}
        for c in configs
    ]


@router.post("/config")
def upsert_config(req: AgentConfigRequest, db: Session = Depends(get_db)) -> Dict[str, str]:
    config = db.query(AgentConfig).filter_by(name=req.name).first()
    if config:
        config.enabled = req.enabled
        config.settings = req.settings
    else:
        config = AgentConfig(name=req.name, enabled=req.enabled, settings=req.settings)
        db.add(config)
    db.commit()
    return {"status": "saved"}


class EnableRequest(BaseModel):
    name: str
    enabled: bool


@router.post("/enable")
def set_enabled(req: EnableRequest, db: Session = Depends(get_db)) -> Dict[str, str]:
    config = db.query(AgentConfig).filter_by(name=req.name).first()
    if not config:
        raise HTTPException(status_code=404, detail="Agent not found")
    config.enabled = req.enabled
    db.commit()
    return {"status": "updated"}
