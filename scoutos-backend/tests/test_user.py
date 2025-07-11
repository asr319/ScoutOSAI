from fastapi.testclient import TestClient
import sys, os, uuid
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app.main import app

client = TestClient(app)


def test_register_and_login():
    username = f"u_{uuid.uuid4().hex[:8]}"
    password = "pw"

    resp = client.post("/user/register", json={"username": username, "password": password})
    assert resp.status_code == 200
    user_id = resp.json()["id"]

    resp = client.post("/user/login", json={"username": username, "password": password})
    assert resp.status_code == 200
    assert resp.json()["id"] == user_id

