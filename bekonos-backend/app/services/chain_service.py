from __future__ import annotations

from typing import List
from sqlalchemy.orm import Session

from app.models.chain import Chain


class ChainService:
    """Service layer for Chain CRUD operations."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_chain(self, name: str, actions: List[dict]) -> Chain:
        chain = Chain(name=name, actions=actions)
        self.db.add(chain)
        self.db.commit()
        self.db.refresh(chain)
        return chain

    def list_chains(self) -> List[Chain]:
        return self.db.query(Chain).all()

    def get_chain(self, chain_id: int) -> Chain | None:
        return self.db.get(Chain, chain_id)
