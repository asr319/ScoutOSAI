from fastapi.testclient import TestClient
import os, sys, uuid
import pyotp

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from app.main import app  # noqa: E402

client = TestClient(app)


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
