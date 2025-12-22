# aps.py - Analytics Processing Service
from flask import Flask, jsonify
import time
import os

app = Flask(__name__)

# --- Configuration Placeholder ---
DATA_QUEUE_SOURCE = os.environ.get('DATA_QUEUE_SOURCE', 'kafka-topic-raw')
DATA_STORE_TARGET = os.environ.get('DATA_STORE_TARGET', 'clickhouse-db:9000')

# --- Worker Logic ---
def process_data_batch(batch_size: int = 100):
    """Simulates the actual processing of a batch of data."""
    print(f"Processing {batch_size} events from {DATA_QUEUE_SOURCE}...")
    # 1. Read a batch of data from the queue
    # 2. Run calculations (e.g., Pandas logic, SQL queries for aggregation)
    # 3. Write aggregated results to DATA_STORE_TARGET
    time.sleep(random.uniform(1.0, 3.0)) 
    print("Batch processing complete.")
    return batch_size

# --- API Endpoints ---

@app.route('/status', methods=['GET'])
def status():
    # Health check for the worker service
    return jsonify({'status': 'OK', 'processing_target': DATA_STORE_TARGET, 'mode': 'worker'})

@app.route('/trigger_process', methods=['POST'])
def trigger_process():
    # Allows a scheduled job or manual trigger to start a processing run
    process_data_batch(batch_size=500)
    return jsonify({'message': 'Processing batch triggered successfully.'}), 200

if __name__ == '__main__':
    # Typically, the worker loop would run here, but for K8s deployment,
    # we usually start the worker via a separate K8s job or just run the Flask app
    app.run(host='0.0.0.0', port=5001)
