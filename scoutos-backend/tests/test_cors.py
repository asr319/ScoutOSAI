import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_preflight_rejects_disallowed_origin():
    headers = {
        "Origin": "http://evil.test",
        "Access-Control-Request-Method": "GET",
    }
    resp = client.options("/", headers=headers)
    assert resp.status_code == 400
    assert resp.text == "Disallowed CORS origin"


def test_preflight_allows_configured_origin():
    headers = {
        "Origin": "http://allowed.test",
        "Access-Control-Request-Method": "GET",
    }
    resp = client.options("/", headers=headers)
    assert resp.status_code == 200
    assert resp.headers.get("access-control-allow-origin") == (
        "http://allowed.test"
    )
