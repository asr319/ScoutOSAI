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
