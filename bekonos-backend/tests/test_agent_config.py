from fastapi.testclient import TestClient
import os
import sys
import uuid

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from app.main import app  # noqa: E402

client = TestClient(app)


def test_agent_config_crud():
    resp = client.get("/agent/config")
    assert resp.status_code == 200

    name = f"demo_{uuid.uuid4().hex[:8]}"
    resp = client.post(
        "/agent/config",
        json={"name": name, "enabled": True, "settings": {"k": "v"}},
    )
    assert resp.status_code == 200

    resp = client.get("/agent/config")
    assert any(c["name"] == name for c in resp.json())

    resp = client.post(
        "/agent/enable",
        json={"name": name, "enabled": False},
    )
    assert resp.status_code == 200

    resp = client.get("/agent/config")
    cfg = next(c for c in resp.json() if c["name"] == name)
    assert cfg["enabled"] is False
