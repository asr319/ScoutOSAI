from fastapi.testclient import TestClient
import os, sys, uuid
import pyotp

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from app.main import app  # noqa: E402

client = TestClient(app)


def _auth():
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

def test_register_and_login():
    username = f"u_{uuid.uuid4().hex[:8]}"
    password = "pw"

    resp = client.post(
        "/user/register",
        json={"username": username, "password": password},
    )
    assert resp.status_code == 200
    data = resp.json()
    user_id = data["id"]
    totp = pyotp.TOTP(data["totp_secret"]).now()

    resp = client.post(
        "/user/login",
        json={"username": username, "password": password, "totp_code": totp},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["id"] == user_id
    assert "token" in body

def test_profile_get_and_put():
    user_id, token = _auth()
    resp = client.get(
        "/user/profile",
        params={"user_id": user_id},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    assert resp.json() == {"user_id": user_id, "preferences": {}}

    data = {"user_id": user_id, "preferences": {"theme": "dark", "notify": True}}
    resp = client.put(
        "/user/profile",
        json=data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    assert resp.json()["profile"]["preferences"]["theme"] == "dark"

    resp = client.get(
        "/user/profile",
        params={"user_id": user_id},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.json()["preferences"]["theme"] == "dark"


def test_profile_unauthorized():
    user_id, token = _auth()
    other_id, other_token = _auth()

    resp = client.get(
        "/user/profile",
        params={"user_id": user_id},
        headers={"Authorization": f"Bearer {other_token}"},
    )
    assert resp.status_code == 403

    resp = client.put(
        "/user/profile",
        json={"user_id": user_id, "preferences": {}},
        headers={"Authorization": f"Bearer {other_token}"},
    )
    assert resp.status_code == 403
