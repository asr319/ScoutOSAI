import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.db import SessionLocal
from app.services.user_service import UserService
from app.services.memory_service import MemoryService
import uuid


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
    mem = mem_service.add_memory({"user_id": user.id, "content": "c", "topic": "t", "tags": []})

    assert mem.id is not None
    fetched = mem_service.get_memory(mem.id)
    assert fetched.content == "c"

    mem_service.update_memory(mem.id, {"content": "new"})
    updated = mem_service.get_memory(mem.id)
    assert updated.content == "new"

    listed = mem_service.list_memories(user.id)
    assert any(m.id == mem.id for m in listed)

    assert mem_service.delete_memory(mem.id) is True
    assert mem_service.get_memory(mem.id) is None
    db.close()
