# test_dis.py
from fastapi.testclient import TestClient
from dis import app, fetch_external_data

client = TestClient(app)

def test_status_endpoint():
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json()["status"] == "OK"

def test_trigger_ingest_valid():
    # Test triggering an ingest task (it should return immediately, status 200)
    response = client.get("/ingest/shopify")
    assert response.status_code == 200
    assert "initiated" in response.json()["message"]

def test_trigger_ingest_invalid():
    # Test triggering an ingest task with an invalid source
    response = client.get("/ingest/unknown_source")
    assert response.status_code == 400
    assert "Invalid data source" in response.json()["detail"]

def test_fetch_external_data_structure():
    # Test the structure of the simulated fetched data
    data = fetch_external_data("test_source")
    assert "event_id" in data
    assert "timestamp" in data
    assert "source" == "test_source"
    assert "payload" in data
