# dis.py - Data Ingest Service
from fastapi import FastAPI, BackgroundTasks, HTTPException
import time
import random
import os

app = FastAPI(title="Data Ingest Service")

# --- Configuration Placeholder ---
# Represents the message queue endpoint (e.g., Kafka or Redis)
MESSAGE_QUEUE_ENDPOINT = os.environ.get('MESSAGE_QUEUE_ENDPOINT', 'kafka-broker:9092')

# --- Simulated External API Data ---
def fetch_external_data(source: str):
    """Simulates fetching data from an external source API."""
    print(f"[{source}] Attempting to fetch data...")
    time.sleep(random.uniform(0.1, 0.5)) # Simulate network latency
    
    # Simulate data payload
    data = {
        "event_id": str(random.randint(1000, 9999)),
        "timestamp": time.time(),
        "source": source,
        "payload": {"clicks": random.randint(100, 500), "cost_usd": round(random.uniform(50, 200), 2)}
    }
    return data

def push_to_queue(data: dict):
    """Simulates pushing normalized data to the message queue."""
    # In a real app, this would use a Kafka Producer or similar client library
    print(f"Successfully pushed data to {MESSAGE_QUEUE_ENDPOINT}: {data['event_id']}")
    return True

async def background_ingest_task(source: str):
    """The actual asynchronous ingestion and queuing logic."""
    try:
        raw_data = fetch_external_data(source)
        if raw_data:
            push_to_queue(raw_data)
        return True
    except Exception as e:
        print(f"Ingest failed for {source}: {str(e)}")
        return False

# --- API Endpoints ---

@app.get("/ingest/{source}", tags=["Ingestion"])
async def trigger_ingest(source: str, background_tasks: BackgroundTasks):
    """Triggers an asynchronous data ingestion run for a given source."""
    if source not in ['shopify', 'google_ads', 'billing']:
        raise HTTPException(status_code=400, detail="Invalid data source specified.")

    # Execute the heavy lifting asynchronously to free up the API thread
    background_tasks.add_task(background_ingest_task, source)
    
    return {"message": f"Ingestion task initiated for {source}. Check queue for results."}

@app.get("/status", tags=["Health"])
async def get_status():
    return {"status": "OK", "queue_target": MESSAGE_QUEUE_ENDPOINT}
