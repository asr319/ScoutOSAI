from fastapi.testclient import TestClient
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app.main import app

client = TestClient(app)


def test_merge_endpoint():
    d1 = {"user_id": 1, "content": "a", "topic": "t", "tags": ["x"]}
    d2 = {"user_id": 1, "content": "b", "topic": "t", "tags": ["y"]}
    r1 = client.post("/memory/add", json=d1)
    r2 = client.post("/memory/add", json=d2)
    ids = [r1.json()["memory"]["id"], r2.json()["memory"]["id"]]
    resp = client.post("/agent/merge", json={"user_id": 1, "memory_ids": ids})
    assert resp.status_code == 200
    body = resp.json()["memory"]
    assert "a" in body["content"] and "b" in body["content"]
    assert set(body["tags"]) == {"x", "y"}


def test_merge_endpoint_unauthorized():
    d1 = {"user_id": 10, "content": "a", "topic": "t", "tags": []}
    d2 = {"user_id": 10, "content": "b", "topic": "t", "tags": []}
    r1 = client.post("/memory/add", json=d1)
    r2 = client.post("/memory/add", json=d2)
    ids = [r1.json()["memory"]["id"], r2.json()["memory"]["id"]]
    resp = client.post("/agent/merge", json={"user_id": 11, "memory_ids": ids})
    assert resp.status_code == 403
