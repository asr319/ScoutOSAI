from fastapi.testclient import TestClient
import os
import sys

from app.services import agent_service

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from app.main import app  # noqa: E402
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

    async def fake_create(*_: str, **__: str):
        return fake_resp

    fake_client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(create=fake_create)
        )
    )

    monkeypatch.setattr(agent_service, "AsyncOpenAI", lambda **_: fake_client)

    resp = client.post("/ai/chat", json={"prompt": "hi"})
    assert resp.status_code == 200
    assert resp.json() == {"response": "mocked reply"}


def test_ai_tags_missing_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    resp = client.post("/ai/tags", json={"text": "memo"})
    assert resp.status_code == 500
    assert "OPENAI_API_KEY" in resp.json()["detail"]


def test_ai_tags_returns_mocked_tags(monkeypatch):
    from types import SimpleNamespace

    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")

    fake_resp = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content="x, y"))]
    )

    async def fake_acreate(*_: str, **__: str):
        return fake_resp

    fake_client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(acreate=fake_acreate)
        )
    )

    monkeypatch.setattr(agent_service, "AsyncOpenAI", lambda **_: fake_client)

    resp = client.post("/ai/tags", json={"text": "text"})
    assert resp.status_code == 200
    assert resp.json() == {"tags": ["x", "y"]}


def test_ai_merge_missing_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    from types import SimpleNamespace
    class FakeService:
        def __init__(self, _db):
            pass

        def get_memory(self, mid):
            return SimpleNamespace(content=f"m{mid}")

    monkeypatch.setattr(ai_module, "MemoryService", FakeService)

    resp = client.post("/ai/merge", json={"memory_ids": [1, 2]})
    assert resp.status_code == 500
    assert "OPENAI_API_KEY" in resp.json()["detail"]


def test_ai_merge_returns_mocked_text(monkeypatch):
    from types import SimpleNamespace

    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")

    fake_resp = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content="merge"))]
    )

    async def fake_acreate(*_: str, **__: str):
        return fake_resp

    fake_client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(acreate=fake_acreate)
        )
    )

    class FakeService:
        def __init__(self, _db):
            pass

        def get_memory(self, mid):
            return SimpleNamespace(content=f"mem{mid}")

    monkeypatch.setattr(ai_module, "MemoryService", FakeService)

    monkeypatch.setattr(ai_module, "AsyncOpenAI", lambda **_: fake_client)

    resp = client.post("/ai/merge", json={"memory_ids": [1, 2]})
    assert resp.status_code == 200
    assert resp.json() == {"verdict": "merge"}


def test_ai_summary_missing_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    resp = client.post("/ai/summary", json={"content": "abc"})
    assert resp.status_code == 500
    assert "OPENAI_API_KEY" in resp.json()["detail"]


def test_ai_summary_returns_mocked_text(monkeypatch):
    from types import SimpleNamespace

    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")

    fake_resp = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content="summary"))]
    )

    async def fake_acreate(*_: str, **__: str):
        return fake_resp

    fake_client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(acreate=fake_acreate)
        )
    )

    monkeypatch.setattr(agent_service, "AsyncOpenAI", lambda **_: fake_client)

    resp = client.post("/ai/summary", json={"content": "the text"})
    assert resp.status_code == 200
    assert resp.json() == {"summary": "summary"}


def test_ai_chat_async_returns_mocked_text(monkeypatch):
    """POST /ai/chat should support AsyncOpenAI.acreate."""
    from types import SimpleNamespace

    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")

    fake_resp = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content="async reply"))]
    )

    async def fake_acreate(*_: str, **__: str):
        return fake_resp

    fake_client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(acreate=fake_acreate)
        )
    )

    monkeypatch.setattr(agent_service, "AsyncOpenAI", lambda **_: fake_client)

    resp = client.post("/ai/chat", json={"prompt": "hello"})
    assert resp.status_code == 200
    assert resp.json() == {"response": "async reply"}


def test_ai_chat_handles_openai_error(monkeypatch):
    """POST /ai/chat should return 503 if OpenAI raises an exception."""
    from types import SimpleNamespace

    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")

    async def fake_create(*_: str, **__: str):
        raise Exception("boom")

    fake_client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(create=fake_create)
        )
    )

    monkeypatch.setattr(agent_service, "AsyncOpenAI", lambda **_: fake_client)

    resp = client.post("/ai/chat", json={"prompt": "boom"})
    assert resp.status_code == 503
    assert "OpenAI request failed" in resp.json()["detail"]

