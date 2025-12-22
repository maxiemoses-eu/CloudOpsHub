# das.py - Data API Service (FastAPI)
from fastapi import FastAPI, HTTPException
from typing import List, Dict
import os

app = FastAPI(title="Data API Service")

# --- Configuration Placeholder ---
# In a real scenario, this service connects to the Analytics Processing Service's 
# low-latency data store (e.g., ClickHouse or a specialized data warehouse).
DATA_STORE_URL = os.environ.get('DATA_STORE_URL', 'http://analytics-store:8080')

# --- Dummy Data Structure for Demonstration ---
# This data structure would normally be loaded dynamically from the data store.
DUMMY_DATA = [
    {"date": "2025-11-01", "revenue": 15000, "conversion_rate": 0.04},
    {"date": "2025-11-02", "revenue": 18500, "conversion_rate": 0.05},
    {"date": "2025-11-03", "revenue": 17000, "conversion_rate": 0.045},
]

# --- API Endpoints ---

@app.get("/status", tags=["Health"])
async def get_status():
    # Simple check to confirm service is running
    return {"status": "OK", "data_source": DATA_STORE_URL}

@app.get("/metrics/daily", response_model=List[Dict])
async def get_daily_metrics(start_date: str = None, end_date: str = None):
    """
    Retrieves aggregated daily revenue and conversion metrics.
    """
    # In a real app: Query the data store based on date filters (start_date, end_date)
    
    # For now, return the dummy data
    if not DUMMY_DATA:
         raise HTTPException(status_code=404, detail="No metrics found.")
         
    return DUMMY_DATA

@app.get("/metrics/cltv")
async def get_customer_lifetime_value():
    """
    Retrieves the calculated Customer Lifetime Value (CLTV).
    """
    # In a real app: Query the data store for the CLTV calculation
    return {"cltv_usd": 785.50, "calculation_date": "2025-12-12"}
