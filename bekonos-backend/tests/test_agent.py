import os, sys, uuid
from fastapi.testclient import TestClient

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from app.main import app  # noqa: E402

client = TestClient(app)

import pyotp


def _auth(role: str = "user"):
    username = f"u_{uuid.uuid4().hex[:8]}"
    r = client.post(
        "/user/register",
        json={"username": username, "password": "pw", "role": role},
    )
    body = r.json()
    user_id = body["id"]
    totp = pyotp.TOTP(body["totp_secret"]).now()
    r = client.post(
        "/user/login",
        json={"username": username, "password": "pw", "totp_code": totp},
    )
    token = r.json()["token"]
    return user_id, token


def test_merge_endpoint():
    user_id, token = _auth()
    d1 = {"user_id": user_id, "content": "a", "topic": "t", "tags": ["x"]}
    d2 = {"user_id": user_id, "content": "b", "topic": "t", "tags": ["y"]}
    r1 = client.post(
        "/memory/add",
        json=d1,
        headers={"Authorization": f"Bearer {token}"},
    )
    r2 = client.post(
        "/memory/add",
        json=d2,
        headers={"Authorization": f"Bearer {token}"},
    )
    ids = [r1.json()["memory"]["id"], r2.json()["memory"]["id"]]
    resp = client.post(
        "/agent/merge",
        json={"user_id": user_id, "memory_ids": ids},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    body = resp.json()["memory"]
    assert "a" in body["content"] and "b" in body["content"]
    assert set(body["tags"]) == {"x", "y"}


def test_merge_endpoint_unauthorized():
    user_id, token = _auth()
    d1 = {"user_id": user_id, "content": "a", "topic": "t", "tags": []}
    d2 = {"user_id": user_id, "content": "b", "topic": "t", "tags": []}
    r1 = client.post(
        "/memory/add",
        json=d1,
        headers={"Authorization": f"Bearer {token}"},
    )
    r2 = client.post(
        "/memory/add",
        json=d2,
        headers={"Authorization": f"Bearer {token}"},
    )
    ids = [r1.json()["memory"]["id"], r2.json()["memory"]["id"]]

    other_id, other_token = _auth()
    resp = client.post(
        "/agent/merge",
        json={"user_id": user_id, "memory_ids": ids},
        headers={"Authorization": f"Bearer {other_token}"},
    )
    assert resp.status_code == 403
