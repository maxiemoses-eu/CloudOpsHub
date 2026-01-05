from fastapi.testclient import TestClient
from das import app

client = TestClient(app)

def test_health_probes():
    assert client.get("/health").status_code == 200
    assert client.get("/ready").status_code == 200

def test_status_endpoint():
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json()["status"] == "OK"

def test_metrics():
    response = client.get("/metrics/daily")
    assert response.status_code == 200
    assert len(response.json()) > 0