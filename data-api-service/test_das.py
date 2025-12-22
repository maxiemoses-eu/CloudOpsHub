# test_das.py
from fastapi.testclient import TestClient
from das import app

client = TestClient(app)

def test_status_endpoint():
    # Test the basic health status
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json()["status"] == "OK"

def test_daily_metrics_endpoint():
    # Test successful retrieval of daily metrics
    response = client.get("/metrics/daily")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    assert "revenue" in response.json()[0]

def test_cltv_endpoint():
    # Test the CLTV endpoint structure
    response = client.get("/metrics/cltv")
    assert response.status_code == 200
    data = response.json()
    assert "cltv_usd" in data
    assert isinstance(data["cltv_usd"], float)
