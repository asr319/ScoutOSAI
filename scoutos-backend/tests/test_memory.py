from fastapi.testclient import TestClient
import sys, os, uuid
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app.main import app

client = TestClient(app)

def test_add_memory():
    data = {"user_id": 1, "content": "test", "topic": "t", "tags": []}
    resp = client.post("/memory/add", json=data)
    assert resp.status_code == 200
    assert resp.json()["memory"]["content"] == "test"


def test_update_memory():
    data = {"user_id": 1, "content": "init", "topic": "t", "tags": []}
    resp = client.post("/memory/add", json=data)
    memory_id = resp.json()["memory"]["id"]

    updated = {"user_id": 1, "content": "updated", "topic": "t", "tags": []}
    resp = client.put(f"/memory/update/{memory_id}", json=updated)
    assert resp.status_code == 200
    assert resp.json()["memory"]["content"] == "updated"


def test_list_memories_returns_for_user():
    user_id = 1000 + int(uuid.uuid4().hex[:6], 16)

    entries = [
        {"content": "a", "topic": "alpha", "tags": ["urgent"]},
        {"content": "b", "topic": "alpha", "tags": ["later"]},
        {"content": "c", "topic": "beta", "tags": ["urgent"]},
    ]
    for e in entries:
        data = {"user_id": user_id, **e}
        client.post("/memory/add", json=data)

    resp = client.get("/memory/list", params={"user_id": user_id})
    assert resp.status_code == 200
    memories = resp.json()
    assert len(memories) == len(entries)
    contents = {m["content"] for m in memories}
    assert contents == {"a", "b", "c"}


def test_search_memory_filters_by_topic_and_tag():
    user_id = 2000 + int(uuid.uuid4().hex[:6], 16)

    mems = [
        {"content": "a", "topic": "alpha", "tags": ["urgent"]},
        {"content": "b", "topic": "alpha", "tags": ["later"]},
        {"content": "c", "topic": "beta", "tags": ["urgent"]},
    ]
    for m in mems:
        client.post("/memory/add", json={"user_id": user_id, **m})

    by_topic = client.get("/memory/search", params={"user_id": user_id, "topic": "alpha"})
    assert {m["content"] for m in by_topic.json()} == {"a", "b"}

    by_tag = client.get("/memory/search", params={"user_id": user_id, "tag": "urgent"})
    assert {m["content"] for m in by_tag.json()} == {"a", "c"}

    both = client.get(
        "/memory/search",
        params={"user_id": user_id, "topic": "alpha", "tag": "later"},
    )
    assert [m["content"] for m in both.json()] == ["b"]
