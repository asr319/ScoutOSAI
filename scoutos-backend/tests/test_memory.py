from fastapi.testclient import TestClient
import sys, os
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


def test_list_and_search_memory():
    data = {"user_id": 2, "content": "hello", "topic": "greet", "tags": ["a"]}
    client.post("/memory/add", json=data)

    list_resp = client.get("/memory/list", params={"user_id": 2})
    assert list_resp.status_code == 200
    assert isinstance(list_resp.json(), list)
    assert list_resp.json()[0]["content"] == "hello"

    search_resp = client.get(
        "/memory/search",
        params={"user_id": 2, "topic": "greet", "tag": "a"},
    )
    assert search_resp.status_code == 200
    assert search_resp.json()[0]["topic"] == "greet"
