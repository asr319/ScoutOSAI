import uuid
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _auth():
    username = f"u_{uuid.uuid4().hex[:8]}"
    password = "pw"
    r = client.post("/user/register", json={"username": username, "password": password})
    user_id = r.json()["id"]
    r = client.post("/user/login", json={"username": username, "password": password})
    token = r.json()["token"]
    return user_id, token


def test_memory_event_via_websocket():
    user_id, token = _auth()
    with client.websocket_connect(f"/ws/{user_id}") as ws:
        data = {"user_id": user_id, "content": "wstest", "topic": "t", "tags": []}
        resp = client.post("/memory/add", json=data, headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        message = ws.receive_json()
        assert message["type"] == "memory"
        assert message["action"] == "added"
