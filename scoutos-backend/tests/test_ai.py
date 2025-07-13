from fastapi.testclient import TestClient
import os
import sys
from app.routes import ai as ai_module

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from app.main import app  # noqa: E402

client = TestClient(app)


def test_ai_missing_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    resp = client.post("/ai/chat", json={"prompt": "hello"})
    assert resp.status_code == 500
    assert "OPENAI_API_KEY" in resp.json()["detail"]


def test_ai_chat_returns_mocked_text(monkeypatch):
    """POST /ai/chat should return the text from the mocked OpenAI API."""
    from types import SimpleNamespace

    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")

    fake_resp = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content="mocked reply"))]
    )

    async def fake_acreate(**_: str):
        return fake_resp

    monkeypatch.setattr(openai.ChatCompletion, "acreate", fake_acreate)

    resp = client.post("/ai/chat", json={"prompt": "hi"})
    assert resp.status_code == 200
    assert resp.json() == {"response": "mocked reply"}
