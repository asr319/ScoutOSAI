import os
import sys
from app.models.memory import Memory
import uuid

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.db import SessionLocal  # noqa: E402
from app.services.user_service import UserService  # noqa: E402
from app.services.memory_service import MemoryService  # noqa: E402


def test_user_service_create_and_get():
    db = SessionLocal()
    service = UserService(db)
    username = f"alice_{uuid.uuid4().hex[:8]}"
    user = service.create_user({"username": username, "password": "secret"})

    assert user.id is not None
    assert user.password_hash != "secret"
    fetched = service.get_by_username(username)
    assert fetched.id == user.id
    db.close()


def test_user_service_password_verify():
    db = SessionLocal()
    service = UserService(db)
    username = f"charlie_{uuid.uuid4().hex[:8]}"
    user = service.create_user({"username": username, "password": "secret"})

    assert service.pw_hasher.verify(user.password_hash, "secret")
    db.close()


def test_memory_service_crud():
    db = SessionLocal()
    user_service = UserService(db)
    username = f"bob_{uuid.uuid4().hex[:8]}"
    user = user_service.create_user({"username": username, "password": "pw"})

    mem_service = MemoryService(db)
    mem = mem_service.add_memory(
        {"user_id": user.id, "content": "c", "topic": "t", "tags": []}
    )

    assert mem.id is not None
    raw = SessionLocal()
    stored = raw.get(Memory, mem.id)
    assert stored.content != "c"
    raw.close()
    fetched = mem_service.get_memory(mem.id)
    assert fetched.content == "c"

    mem_service.update_memory(mem.id, user.id, {"content": "new"})
    updated = mem_service.get_memory(mem.id)
    assert updated.content == "new"
    raw = SessionLocal()
    stored = raw.get(Memory, mem.id)
    assert stored.content != "new"
    raw.close()

    listed = mem_service.list_memories(user.id)
    assert any(m.id == mem.id for m in listed)

    assert mem_service.delete_memory(mem.id, user.id) is True
    assert mem_service.get_memory(mem.id) is None
    db.close()


def test_memory_service_unauthorized_operations():
    db = SessionLocal()
    user_service = UserService(db)
    user_a = user_service.create_user({"username": "ua", "password": "pw"})
    user_b = user_service.create_user({"username": "ub", "password": "pw"})

    mem_service = MemoryService(db)
    mem = mem_service.add_memory({"user_id": user_a.id, "content": "c", "topic": "t", "tags": []})

    assert mem_service.update_memory(mem.id, user_b.id, {"content": "bad"}) is None
    assert mem_service.delete_memory(mem.id, user_b.id) is False
    # cleanup
    mem_service.delete_memory(mem.id, user_a.id)
    db.close()


def test_memory_service_merge():
    db = SessionLocal()
    user_service = UserService(db)
    username = f"merge_{uuid.uuid4().hex[:8]}"
    user = user_service.create_user({"username": username, "password": "pw"})

    mem_service = MemoryService(db)
    m1 = mem_service.add_memory(
        {"user_id": user.id, "content": "a", "topic": "t", "tags": ["x"]}
    )
    m2 = mem_service.add_memory(
        {"user_id": user.id, "content": "b", "topic": "t", "tags": ["y"]}
    )

    merged = mem_service.merge_memories([m1.id, m2.id], user.id)
    assert merged.content == "a\nb"
    assert set(merged.tags) == {"x", "y"}
    raw = SessionLocal()
    stored = raw.get(Memory, merged.id)
    assert stored.content != "a\nb"
    raw.close()
    assert mem_service.get_memory(m1.id) is None
    assert mem_service.get_memory(m2.id) is None
    db.close()


def test_merge_memories_user_mismatch():
    db = SessionLocal()
    user_service = UserService(db)
    u1 = user_service.create_user({"username": f"u1_{uuid.uuid4().hex[:8]}", "password": "pw"})
    u2 = user_service.create_user({"username": f"u2_{uuid.uuid4().hex[:8]}", "password": "pw"})

    mem_service = MemoryService(db)
    m1 = mem_service.add_memory({"user_id": u1.id, "content": "a", "topic": "t", "tags": []})
    m2 = mem_service.add_memory({"user_id": u2.id, "content": "b", "topic": "t", "tags": []})

    merged = mem_service.merge_memories([m1.id, m2.id], u1.id)
    assert merged is None
    assert mem_service.get_memory(m1.id) is not None
    assert mem_service.get_memory(m2.id) is not None
    db.close()


def test_merge_memories_user_mismatch():
    db = SessionLocal()
    user_service = UserService(db)
    u1 = user_service.create_user(
        {"username": f"u1_{uuid.uuid4().hex[:8]}", "password": "pw"}
    )
    u2 = user_service.create_user(
        {"username": f"u2_{uuid.uuid4().hex[:8]}", "password": "pw"}
    )

    mem_service = MemoryService(db)
    m1 = mem_service.add_memory(
        {"user_id": u1.id, "content": "a", "topic": "t", "tags": []}
    )
    m2 = mem_service.add_memory(
        {"user_id": u2.id, "content": "b", "topic": "t", "tags": []}
    )

    merged = mem_service.merge_memories([m1.id, m2.id], u1.id)
    assert merged is None
    assert mem_service.get_memory(m1.id) is not None
    assert mem_service.get_memory(m2.id) is not None
    db.close()
