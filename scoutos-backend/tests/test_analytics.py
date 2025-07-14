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
