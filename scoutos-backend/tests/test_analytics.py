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


def test_memory_add_creates_event():
    user_id, token = _auth()
    client.post(
        "/memory/add",
        json={"user_id": user_id, "content": "a", "topic": "t", "tags": []},
        headers={"Authorization": f"Bearer {token}"},
    )
    resp = client.get("/analytics/events", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    events = resp.json()
    assert any(e["event_type"] == "memory_created" for e in events)


def test_summary_endpoint_counts_events():
    user_id, token = _auth()
    for _ in range(2):
        client.post(
            "/memory/add",
            json={"user_id": user_id, "content": "x", "topic": "t", "tags": []},
            headers={"Authorization": f"Bearer {token}"},
        )
    resp = client.get("/analytics/summary", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("memory_created") >= 2
