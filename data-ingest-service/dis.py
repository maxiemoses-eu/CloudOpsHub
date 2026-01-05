from fastapi import FastAPI, BackgroundTasks, HTTPException
import time
import random
import os

app = FastAPI(title="Data Ingest Service")

# --- Configuration Aligned with Helm ---
MESSAGE_QUEUE_ENDPOINT = os.environ.get('MESSAGE_QUEUE_ENDPOINT', 'kafka-broker:9092')
PORT = int(os.environ.get('PORT', 8001))

def fetch_external_data(source: str):
    time.sleep(random.uniform(0.1, 0.5)) 
    data = {
        "event_id": str(random.randint(1000, 9999)),
        "timestamp": time.time(),
        "source": source,
        "payload": {"clicks": random.randint(100, 500), "cost_usd": round(random.uniform(50, 200), 2)}
    }
    return data

def push_to_queue(data: dict):
    print(f"Successfully pushed data to {MESSAGE_QUEUE_ENDPOINT}: {data['event_id']}")
    return True

async def background_ingest_task(source: str):
    try:
        raw_data = fetch_external_data(source)
        if raw_data:
            push_to_queue(raw_data)
        return True
    except Exception as e:
        print(f"Ingest failed for {source}: {str(e)}")
        return False

# --- Standardized Health Endpoints ---

@app.get("/health", tags=["Health"])
async def health():
    """Liveness Probe"""
    return {"status": "alive"}

@app.get("/ready", tags=["Health"])
async def ready():
    """Readiness Probe - Check Queue Connectivity"""
    return {"status": "ready", "queue": MESSAGE_QUEUE_ENDPOINT}

@app.get("/status", tags=["Health"])
async def get_status():
    return {"status": "OK", "queue_target": MESSAGE_QUEUE_ENDPOINT}

@app.get("/ingest/{source}", tags=["Ingestion"])
async def trigger_ingest(source: str, background_tasks: BackgroundTasks):
    if source not in ['shopify', 'google_ads', 'billing']:
        raise HTTPException(status_code=400, detail="Invalid data source specified.")
    background_tasks.add_task(background_ingest_task, source)
    return {"message": f"Ingestion task initiated for {source}."}