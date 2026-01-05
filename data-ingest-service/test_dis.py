from fastapi.testclient import TestClient
from dis import app

client = TestClient(app)

def test_health_paths():
    assert client.get("/health").status_code == 200
    assert client.get("/ready").status_code == 200

def test_trigger_ingest_flow():
    response = client.get("/ingest/shopify")
    assert response.status_code == 200
    assert "initiated" in response.json()["message"]