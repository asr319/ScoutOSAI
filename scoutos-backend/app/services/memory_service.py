# Placeholder for memory-related business logic

"""Business logic for memory records with encryption."""

from __future__ import annotations

import datetime
import os
from typing import List

from cryptography.fernet import Fernet
from sqlalchemy.orm import Session

from app.models.memory import Memory
from app.utils.encryption import encrypt_text, decrypt_text

# Deterministic fallback key so tests work without configuration
DEFAULT_KEY = b"1OGaT5SwPuHVrxTp1lT7ZnkSeBAkiqdSqsgTbDuSwIs="


class MemoryService:
    """Service layer for ``Memory`` CRUD operations and utilities."""

    def __init__(self, db: Session, key: str | None = None) -> None:
        self.db = db
        fernet_key = key or os.getenv("FERNET_KEY") or DEFAULT_KEY
        if isinstance(fernet_key, str):
            fernet_key = fernet_key.encode()
        self.fernet = Fernet(fernet_key)

    def add_memory(self, memory_data: dict) -> Memory:
        """Create and persist a new ``Memory`` record."""
        encrypted = self.fernet.encrypt(memory_data["content"].encode()).decode()

        db_mem = Memory(
            user_id=memory_data["user_id"],
            content=encrypt_text(encrypted),
            topic=memory_data.get("topic", ""),
            tags=memory_data.get("tags", []),
            timestamp=datetime.datetime.now(tz=datetime.timezone.utc),
        )
        self.db.add(db_mem)
        self.db.commit()
        self.db.refresh(db_mem)
        return self._decrypt_mem(db_mem)

    def _decrypt_mem(self, mem: Memory) -> Memory:
        """Return a memory with decrypted ``content`` field."""
        if mem and isinstance(mem.content, str):
            try:
                inner = decrypt_text(mem.content)
                mem.content = self.fernet.decrypt(inner.encode()).decode()
            except Exception:
                pass
        return mem

    def get_memory(self, memory_id: int) -> Memory | None:
        """Retrieve a ``Memory`` by primary key."""
        mem = self.db.get(Memory, memory_id)
        return self._decrypt_mem(mem)

    def list_memories(self, user_id: int) -> List[Memory]:
        """Return all ``Memory`` rows for a given user."""

        mems = self.db.query(Memory).filter(Memory.user_id == user_id).all()
        return [self._decrypt_mem(m) for m in mems]

    def search_memories(
        self,
        user_id: int,
        topic: str | None = None,
        tag: str | None = None,
        content: str | None = None,
    ) -> List[Memory]:
        """Return memories for ``user_id`` filtered by ``topic``, ``tag`` or ``content``."""

        query = self.db.query(Memory).filter(Memory.user_id == user_id)
        if topic is not None:
            query = query.filter(Memory.topic == topic)
        if tag is not None:
            query = query.filter(Memory.tags.contains([tag]))

        mems = [self._decrypt_mem(m) for m in query.all()]

        if content is not None:
            lowered = content.lower()
            mems = [m for m in mems if lowered in m.content.lower()]
        return mems

    def update_memory(self, memory_id: int, user_id: int, updates: dict) -> Memory | None:
        """Update an existing ``Memory`` with provided values if owned by ``user_id``."""

        mem = self.db.get(Memory, memory_id)
        if not mem or mem.user_id != user_id:
            return None
        for key, value in updates.items():
            if key == "content":
                value = self.fernet.encrypt(value.encode()).decode()
            if hasattr(mem, key):
                if key == "content":
                    setattr(mem, key, encrypt_text(value))
                else:
                    setattr(mem, key, value)
        self.db.commit()
        self.db.refresh(mem)
        self.db.expunge(mem)
        return self._decrypt_mem(mem)

    def delete_memory(self, memory_id: int, user_id: int) -> bool:
        """Delete a ``Memory`` by id if owned by ``user_id``."""

        mem = self.db.get(Memory, memory_id)
        if not mem or mem.user_id != user_id:
            return False
        self.db.delete(mem)
        self.db.commit()
        return True

    def merge_memories(
        self, memory_ids: List[int], user_id: int
    ) -> Memory | None:
        """Merge multiple ``Memory`` rows into one.

        The contents of all memories are concatenated and their tags are
        aggregated into a unique set. The merge only occurs if all memories
        belong to ``user_id``.
        """

        if not memory_ids:
            return None

        mems = self.db.query(Memory).filter(Memory.id.in_(memory_ids)).all()
        if len(mems) != len(memory_ids):
            return None
        if any(m.user_id != user_id for m in mems):
            return None

        for m in mems:
            self._decrypt_mem(m)

        content = "\n".join(m.content for m in mems)

        tags: set[str] = set()
        for m in mems:
            tags.update(m.tags or [])

        topic = mems[0].topic if mems else ""

        encrypted = self.fernet.encrypt(content.encode()).decode()
        merged = Memory(
            user_id=user_id,
            content=encrypt_text(encrypted),
            topic=topic,
            tags=list(tags),
            timestamp=datetime.datetime.now(tz=datetime.timezone.utc),
        )
        self.db.add(merged)
        for m in mems:
            self.db.delete(m)
        self.db.commit()
        self.db.refresh(merged)
        self.db.expunge(merged)
        return self._decrypt_mem(merged)
