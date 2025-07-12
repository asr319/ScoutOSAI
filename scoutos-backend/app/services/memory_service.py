# Placeholder for memory-related business logic

from typing import List
from sqlalchemy.orm import Session
from app.models.memory import Memory
import datetime
from app.utils.encryption import encrypt_text, decrypt_text


class MemoryService:
    """Service layer for ``Memory`` CRUD operations and utilities."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def add_memory(self, memory_data: dict) -> Memory:
        """Create and persist a new ``Memory`` record."""

        db_mem = Memory(
            user_id=memory_data["user_id"],
            content=encrypt_text(memory_data["content"]),
            topic=memory_data.get("topic", ""),
            tags=memory_data.get("tags", []),
            timestamp=datetime.datetime.utcnow(),
        )
        self.db.add(db_mem)
        self.db.commit()
        self.db.refresh(db_mem)
        decrypted = decrypt_text(db_mem.content)
        self.db.expunge(db_mem)
        db_mem.content = decrypted
        return db_mem

    def get_memory(self, memory_id: int) -> Memory | None:
        """Retrieve a ``Memory`` by primary key."""

        mem = self.db.get(Memory, memory_id)
        if mem:
            decrypted = decrypt_text(mem.content)
            self.db.expunge(mem)
            mem.content = decrypted
        return mem

    def list_memories(self, user_id: int) -> List[Memory]:
        """Return all ``Memory`` rows for a given user."""

        mems = self.db.query(Memory).filter(Memory.user_id == user_id).all()
        result: List[Memory] = []
        for m in mems:
            decrypted = decrypt_text(m.content)
            self.db.expunge(m)
            m.content = decrypted
            result.append(m)
        return result

    def update_memory(self, memory_id: int, updates: dict) -> Memory | None:
        """Update an existing ``Memory`` with provided values."""

        mem = self.db.get(Memory, memory_id)
        if not mem:
            return None
        for key, value in updates.items():
            if hasattr(mem, key):
                if key == "content":
                    setattr(mem, key, encrypt_text(value))
                else:
                    setattr(mem, key, value)
        self.db.commit()
        self.db.refresh(mem)
        decrypted = decrypt_text(mem.content)
        self.db.expunge(mem)
        mem.content = decrypted
        return mem

    def delete_memory(self, memory_id: int) -> bool:
        """Delete a ``Memory`` by id."""

        mem = self.db.get(Memory, memory_id)
        if not mem:
            return False
        self.db.delete(mem)
        self.db.commit()
        return True

    def merge_memories(self, memory_ids: List[int], user_id: int) -> Memory | None:
        """Merge multiple ``Memory`` entries into a single one."""

        if not memory_ids:
            return None

        mems = (
            self.db.query(Memory).filter(Memory.id.in_(memory_ids)).all()
        )
        if len(mems) != len(memory_ids):
            return None

        content = "\n".join(decrypt_text(m.content) for m in mems)
        tags = set()
        for m in mems:
            tags.update(m.tags or [])

        topic = mems[0].topic if mems else ""

        merged = Memory(
            user_id=user_id,
            content=encrypt_text(content),
            topic=topic,
            tags=list(tags),
            timestamp=datetime.datetime.utcnow(),
        )
        self.db.add(merged)
        for m in mems:
            self.db.delete(m)
        self.db.commit()
        self.db.refresh(merged)
        decrypted = decrypt_text(merged.content)
        self.db.expunge(merged)
        merged.content = decrypted
        return merged
