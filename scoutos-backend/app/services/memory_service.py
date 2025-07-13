# Placeholder for memory-related business logic

from typing import List
from sqlalchemy.orm import Session
from app.models.memory import Memory
import datetime


class MemoryService:
    """Service layer for ``Memory`` CRUD operations and utilities."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def add_memory(self, memory_data: dict) -> Memory:
        """Create and persist a new ``Memory`` record."""

        db_mem = Memory(
            user_id=memory_data["user_id"],
            content=memory_data["content"],
            topic=memory_data.get("topic", ""),
            tags=memory_data.get("tags", []),
            timestamp=datetime.datetime.utcnow(),
        )
        self.db.add(db_mem)
        self.db.commit()
        self.db.refresh(db_mem)
        return db_mem

    def get_memory(self, memory_id: int) -> Memory | None:
        """Retrieve a ``Memory`` by primary key."""

        return self.db.get(Memory, memory_id)

    def list_memories(self, user_id: int) -> List[Memory]:
        """Return all ``Memory`` rows for a given user."""

        return self.db.query(Memory).filter(Memory.user_id == user_id).all()

    def update_memory(self, memory_id: int, user_id: int, updates: dict) -> Memory | None:
        """Update an existing ``Memory`` with provided values if owned by ``user_id``."""

        mem = self.db.get(Memory, memory_id)
        if not mem or mem.user_id != user_id:
            return None
        for key, value in updates.items():
            if hasattr(mem, key):
                setattr(mem, key, value)
        self.db.commit()
        self.db.refresh(mem)
        return mem

    def delete_memory(self, memory_id: int, user_id: int) -> bool:
        """Delete a ``Memory`` by id if owned by ``user_id``."""

        mem = self.db.get(Memory, memory_id)
        if not mem or mem.user_id != user_id:
            return False
        self.db.delete(mem)
        self.db.commit()
        return True

    def merge_memories(self, memory_ids: List[int], user_id: int) -> Memory | None:
        """Merge multiple ``Memory`` entries into a single one if all belong to ``user_id``."""

        if not memory_ids:
            return None

        mems = (
            self.db.query(Memory).filter(Memory.id.in_(memory_ids)).all()
        )
        if len(mems) != len(memory_ids):
            return None
        if any(m.user_id != user_id for m in mems):
            return None

        content = "\n".join(m.content for m in mems)
        tags = set()
        for m in mems:
            tags.update(m.tags or [])

        topic = mems[0].topic if mems else ""

        merged = Memory(
            user_id=user_id,
            content=content,
            topic=topic,
            tags=list(tags),
            timestamp=datetime.datetime.utcnow(),
        )
        self.db.add(merged)
        for m in mems:
            self.db.delete(m)
        self.db.commit()
        self.db.refresh(merged)
        return merged
