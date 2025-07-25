from fastapi.testclient import TestClient
import os, sys, uuid

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from app.main import app  # noqa: E402

client = TestClient(app)


import pyotp


def _auth(role: str = "user"):
    username = f"u_{uuid.uuid4().hex[:8]}"
    password = "pw"
    r = client.post(
        "/user/register",
        json={"username": username, "password": password, "role": role},
    )
    body = r.json()
    user_id = body["id"]
    totp = pyotp.TOTP(body["totp_secret"]).now()
    r = client.post(
        "/user/login",
        json={"username": username, "password": password, "totp_code": totp},
    )
    token = r.json()["token"]
    return user_id, token


def test_add_memory():
    user_id, token = _auth()
    data = {"user_id": user_id, "content": "test", "topic": "t", "tags": []}
    resp = client.post(
        "/memory/add",
        json=data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    assert resp.json()["memory"]["content"] == "test"


def test_add_memory_unauthorized():
    user_id, token = _auth()
    data = {"user_id": user_id + 1, "content": "bad", "topic": "t", "tags": []}
    resp = client.post(
        "/memory/add",
        json=data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 403


def test_update_memory():
    user_id, token = _auth()
    data = {"user_id": user_id, "content": "init", "topic": "t", "tags": []}
    resp = client.post(
        "/memory/add",
        json=data,
        headers={"Authorization": f"Bearer {token}"},
    )
    memory_id = resp.json()["memory"]["id"]

    updated = {"user_id": user_id, "content": "updated", "topic": "t", "tags": []}
    resp = client.put(
        f"/memory/update/{memory_id}",
        json=updated,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    assert resp.json()["memory"]["content"] == "updated"


def test_update_memory_unauthorized():
    user_id, token = _auth()
    data = {"user_id": user_id, "content": "init", "topic": "t", "tags": []}
    resp = client.post(
        "/memory/add",
        json=data,
        headers={"Authorization": f"Bearer {token}"},
    )
    memory_id = resp.json()["memory"]["id"]

    updated = {
        "user_id": user_id + 1,
        "content": "nope",
        "topic": "t",
        "tags": [],
    }
    resp = client.put(
        f"/memory/update/{memory_id}",
        json=updated,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 403


def test_list_memories_returns_for_user():
    user_id, token = _auth()

    entries = [
        {"content": "a", "topic": "alpha", "tags": ["urgent"]},
        {"content": "b", "topic": "alpha", "tags": ["later"]},
        {"content": "c", "topic": "beta", "tags": ["urgent"]},
    ]
    for e in entries:
        data = {"user_id": user_id, **e}
        client.post(
            "/memory/add",
            json=data,
            headers={"Authorization": f"Bearer {token}"},
        )

    resp = client.get(
        "/memory/list",
        params={"user_id": user_id},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    memories = resp.json()
    assert len(memories) == len(entries)
    contents = {m["content"] for m in memories}
    assert contents == {"a", "b", "c"}


def test_search_memory_filters_by_topic_and_tag():
    user_id, token = _auth()

    mems = [
        {"content": "a", "topic": "alpha", "tags": ["urgent"]},
        {"content": "b", "topic": "alpha", "tags": ["later"]},
        {"content": "c", "topic": "beta", "tags": ["urgent"]},
    ]
    for m in mems:
        client.post(
            "/memory/add",
            json={"user_id": user_id, **m},
            headers={"Authorization": f"Bearer {token}"},
        )

    by_topic = client.get(
        "/memory/search",
        params={"user_id": user_id, "topic": "alpha"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert {m["content"] for m in by_topic.json()} == {"a", "b"}

    by_tag = client.get(
        "/memory/search",
        params={"user_id": user_id, "tag": "urgent"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert {m["content"] for m in by_tag.json()} == {"a", "c"}

    both = client.get(
        "/memory/search",
        params={"user_id": user_id, "topic": "alpha", "tag": "later"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert [m["content"] for m in both.json()] == ["b"]


def test_search_memory_filters_by_content():
    user_id, token = _auth()

    mems = [
        {"content": "find me", "topic": "alpha", "tags": []},
        {"content": "other", "topic": "alpha", "tags": []},
    ]
    for m in mems:
        client.post(
            "/memory/add",
            json={"user_id": user_id, **m},
            headers={"Authorization": f"Bearer {token}"},
        )

    by_content = client.get(
        "/memory/search",
        params={"user_id": user_id, "content": "find"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert [m["content"] for m in by_content.json()] == ["find me"]


def test_search_memory_returns_all_without_filters():
    user_id, token = _auth()

    mems = [
        {"content": "a", "topic": "alpha", "tags": ["urgent"]},
        {"content": "b", "topic": "beta", "tags": ["later"]},
    ]
    for m in mems:
        client.post(
            "/memory/add",
            json={"user_id": user_id, **m},
            headers={"Authorization": f"Bearer {token}"},
        )

    resp = client.get(
        "/memory/search",
        params={"user_id": user_id},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    contents = {m["content"] for m in resp.json()}
    assert contents == {"a", "b"}


def test_delete_memory():
    user_id, token = _auth()
    data = {"user_id": user_id, "content": "d", "topic": "t", "tags": []}
    resp = client.post(
        "/memory/add",
        json=data,
        headers={"Authorization": f"Bearer {token}"},
    )
    memory_id = resp.json()["memory"]["id"]

    resp = client.delete(
        f"/memory/delete/{memory_id}",
        params={"user_id": user_id},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200


def test_delete_memory_unauthorized():
    user_id, token = _auth()
    data = {"user_id": user_id, "content": "e", "topic": "t", "tags": []}
    resp = client.post(
        "/memory/add",
        json=data,
        headers={"Authorization": f"Bearer {token}"},
    )
    memory_id = resp.json()["memory"]["id"]

    other_id, other_token = _auth()
    resp = client.delete(
        f"/memory/delete/{memory_id}",
        params={"user_id": user_id},
        headers={"Authorization": f"Bearer {other_token}"},
    )
    assert resp.status_code == 403
