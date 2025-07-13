from fastapi.testclient import TestClient
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app.main import app
from app.routes import ai as ai_module

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

    async def fake_create(**_):
        return fake_resp

    class FakeCompletions:
        async def create(self, *args, **kwargs):
            return await fake_create()

    class FakeChat:
        def __init__(self):
            self.completions = FakeCompletions()

    class FakeClient:
        def __init__(self, *args, **kwargs):
            self.chat = FakeChat()

    monkeypatch.setattr(ai_module, "AsyncOpenAI", lambda **_: FakeClient())

    resp = client.post("/ai/chat", json={"prompt": "hi"})
    assert resp.status_code == 200
    assert resp.json() == {"response": "mocked reply"}
