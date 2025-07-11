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

        return self.db.get(Memory, memory_id)

    def list_memories(self, user_id: int) -> list[Memory]:
        """Return all memories for a user."""

        return self.db.query(Memory).filter(Memory.user_id == user_id).all()

    def update_memory(self, memory_id: int, update_data: dict) -> Memory | None:
        """Update fields on a ``Memory`` and persist the changes."""

        mem = self.db.get(Memory, memory_id)
        if mem is None:
            return None
        for key, value in update_data.items():
            setattr(mem, key, value)
        self.db.commit()
        self.db.refresh(mem)
        return mem

    def delete_memory(self, memory_id: int) -> bool:
        """Delete a ``Memory`` by id."""

        mem = self.db.get(Memory, memory_id)
        if mem is None:
            return False
        self.db.delete(mem)
        self.db.commit()
        return True

    def merge_memories(self, memory_ids: list[int], user_id: int) -> Memory | None:
        """Merge multiple memories into a single entry and delete the originals."""

        if not memory_ids:
            return None

        mems = (
            self.db.query(Memory)
            .filter(Memory.id.in_(memory_ids), Memory.user_id == user_id)
            .all()
        )

        if not mems:
            return None

        combined_content = "\n".join(m.content for m in mems)
        tags = []
        for m in mems:
            if m.tags:
                tags.extend(m.tags)

        merged = Memory(
            user_id=user_id,
            content=combined_content,
            topic=mems[0].topic,
            tags=list(dict.fromkeys(tags)),
        )
        self.db.add(merged)
        for m in mems:
            self.db.delete(m)
        self.db.commit()
        self.db.refresh(merged)
        return merged
