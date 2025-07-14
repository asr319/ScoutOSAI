import os
import sys
from fastapi.testclient import TestClient

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from app.main import app  # noqa: E402
import uuid

client = TestClient(app)


def test_chain_create_list_and_run(monkeypatch):
    monkeypatch.setenv("AGENT_BACKEND", "local")
    actions = [{"type": "chat", "prompt": "hello"}]
    name = f"chain_{uuid.uuid4().hex[:8]}"
    resp = client.post("/chain/create", json={"name": name, "actions": actions})
    assert resp.status_code == 200
    chain_id = resp.json()["id"]

    resp = client.get("/chain/list")
    assert resp.status_code == 200
    chains = resp.json()
    assert any(c["id"] == chain_id for c in chains)

    resp = client.post("/chain/run", json={"chain_id": chain_id})
    assert resp.status_code == 200
    assert resp.json() == {"results": ["Local model response"]}
