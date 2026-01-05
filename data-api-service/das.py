from fastapi import FastAPI, HTTPException
from typing import List, Dict
import os

app = FastAPI(title="Data API Service")

# Config - Aligned with Helm Environment Variables
DATA_STORE_URL = os.environ.get('DATA_STORE_URL', 'http://analytics-store:8080')
PORT = int(os.environ.get('PORT', 8000))

DUMMY_DATA = [
    {"date": "2025-11-01", "revenue": 15000, "conversion_rate": 0.04},
    {"date": "2025-11-02", "revenue": 18500, "conversion_rate": 0.05},
]

@app.get("/health", tags=["Health"])
async def health():
    """Liveness Probe: Container is alive"""
    return {"status": "alive"}

@app.get("/ready", tags=["Health"])
async def ready():
    """Readiness Probe: Service is ready for traffic"""
    return {"status": "ready"}

@app.get("/status")
async def get_status():
    return {"status": "OK", "data_source": DATA_STORE_URL}

@app.get("/metrics/daily", response_model=List[Dict])
async def get_daily_metrics():
    return DUMMY_DATA