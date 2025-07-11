from fastapi.testclient import TestClient
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app.main import app

client = TestClient(app)

def test_root():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ScoutOSAI backend running"}
