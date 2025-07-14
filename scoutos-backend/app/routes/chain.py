from typing import List, Dict, Generator

from typing import List, Dict, Generator

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.services.chain_service import ChainService
from app.services.agent_service import AgentService

router = APIRouter()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ChainCreate(BaseModel):
    name: str
    actions: List[dict]


@router.post("/create")
async def create_chain(
    req: ChainCreate, db: Session = Depends(get_db)
) -> Dict[str, int]:
    service = ChainService(db)
    chain = service.create_chain(req.name, req.actions)
    return {"id": chain.id}


@router.get("/list")
async def list_chains(db: Session = Depends(get_db)) -> List[Dict]:
    service = ChainService(db)
    chains = service.list_chains()
    return [{"id": c.id, "name": c.name, "actions": c.actions} for c in chains]


class ChainRunRequest(BaseModel):
    chain_id: int


@router.post("/run")
async def run_chain(
    req: ChainRunRequest, db: Session = Depends(get_db)
) -> Dict[str, List]:
    service = ChainService(db)
    chain = service.get_chain(req.chain_id)
    if not chain:
        raise HTTPException(status_code=404, detail="Chain not found")
    agent = AgentService()
    results = await agent.run_pipeline(chain.actions)
    return {"results": results}
