# Placeholder for memory-related business logic

from sqlalchemy.orm import Session
from app.models.memory import Memory


class MemoryService:
    """Service layer for CRUD operations on ``Memory`` objects."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def add_memory(self, memory_data: dict) -> Memory:
        """Create and persist a ``Memory``."""

        db_mem = Memory(**memory_data)
        self.db.add(db_mem)
        self.db.commit()
        self.db.refresh(db_mem)
        return db_mem

    def get_memory(self, memory_id: int) -> Memory | None:
        """Retrieve a ``Memory`` by primary key."""

        return self.db.query(Memory).get(memory_id)

    def list_memories(self, user_id: int) -> list[Memory]:
        """Return all memories for a user."""

        return self.db.query(Memory).filter(Memory.user_id == user_id).all()

    def update_memory(self, memory_id: int, update_data: dict) -> Memory | None:
        """Update fields on a ``Memory`` and persist the changes."""

        mem = self.get_memory(memory_id)
        if mem is None:
            return None
        for key, value in update_data.items():
            setattr(mem, key, value)
        self.db.commit()
        self.db.refresh(mem)
        return mem

    def delete_memory(self, memory_id: int) -> bool:
        """Delete a ``Memory`` by id."""

        mem = self.get_memory(memory_id)
        if mem is None:
            return False
        self.db.delete(mem)
        self.db.commit()
        return True
