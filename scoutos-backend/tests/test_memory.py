from fastapi.testclient import TestClient
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app.main import app

client = TestClient(app)

def test_add_memory():
    data = {"user_id": 1, "content": "test", "topic": "t", "tags": []}
    resp = client.post("/memory/add", json=data)
    assert resp.status_code == 200
    body = resp.json()
    assert "content" in body
    assert body["memory"]["content"] == "test"
    body = resp.json()
    assert body["message"] == "Memory saved"
    assert body["memory"]["content"] == "test"


def test_delete_memory():
    # First add a memory to ensure one exists
    data = {"user_id": 1, "content": "to delete", "topic": "t", "tags": []}
    resp = client.post("/memory/add", json=data)
    assert resp.status_code == 200
    memory_id = resp.json()["memory"]["id"]

    # Delete the memory
    del_resp = client.delete(f"/memory/delete/{memory_id}")
    assert del_resp.status_code == 200
    assert del_resp.json() == {"detail": "Memory deleted"}

    # Verify memory no longer returned from list
    list_resp = client.get("/memory/list", params={"user_id": 1})
    assert list_resp.status_code == 200
    ids = [m["id"] for m in list_resp.json()]
    assert memory_id not in ids
