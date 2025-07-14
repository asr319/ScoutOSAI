from fastapi.testclient import TestClient
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from app.main import app  # noqa: E402

client = TestClient(app)


def test_agent_config_crud():
    resp = client.get("/agent/config")
    assert resp.status_code == 200
    assert resp.json() == []

    resp = client.post(
        "/agent/config",
        json={"name": "demo", "enabled": True, "settings": {"k": "v"}},
    )
    assert resp.status_code == 200

    resp = client.get("/agent/config")
    assert any(c["name"] == "demo" for c in resp.json())

    resp = client.post(
        "/agent/enable",
        json={"name": "demo", "enabled": False},
    )
    assert resp.status_code == 200

    resp = client.get("/agent/config")
    cfg = next(c for c in resp.json() if c["name"] == "demo")
    assert cfg["enabled"] is False
