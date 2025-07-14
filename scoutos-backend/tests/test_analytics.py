from fastapi.testclient import TestClient
import os, sys, uuid
import pyotp

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from app.main import app  # noqa: E402

client = TestClient(app)


def _auth(role: str = "user"):
    username = f"u_{uuid.uuid4().hex[:8]}"
    r = client.post(
        "/user/register",
        json={"username": username, "password": "pw", "role": role},
    )
    body = r.json()
    totp = pyotp.TOTP(body["totp_secret"]).now()
    r = client.post(
        "/user/login",
        json={"username": username, "password": "pw", "totp_code": totp},
    )
    return body["id"], r.json()["token"]


def test_analytics_requires_admin():
    _, token = _auth()
    resp = client.get("/analytics", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 403


def test_analytics_admin_access():
    _, token = _auth("admin")
    resp = client.get("/analytics", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    body = resp.json()
    assert "users" in body and "memories" in body


def _auth_simple():
    username = f"u_{uuid.uuid4().hex[:8]}"
    password = "pw"
    r = client.post(
        "/user/register", json={"username": username, "password": password}
    )
    body = r.json()
    totp = pyotp.TOTP(body["totp_secret"]).now()
    r = client.post(
        "/user/login",
        json={"username": username, "password": password, "totp_code": totp},
    )
    return body["id"], r.json()["token"]


def test_memory_add_creates_event():
    user_id, token = _auth_simple()
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
    user_id, token = _auth_simple()
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
