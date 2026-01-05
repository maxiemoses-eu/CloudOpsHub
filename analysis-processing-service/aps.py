from flask import Flask, jsonify
import os
import time
import random

app = Flask(__name__)

# Config - Aligned with Helm Port
PORT = int(os.environ.get('PORT', 5000))

@app.route('/health', methods=['GET'])
def health():
    """Liveness Probe: Confirms the container is running."""
    return jsonify({"status": "alive"}), 200

@app.route('/ready', methods=['GET'])
def ready():
    """Readiness Probe: Confirms the service is ready to accept traffic."""
    # Add logic here to check DB connection if needed
    return jsonify({"status": "ready"}), 200

@app.route('/status', methods=['GET'])
def status():
    """General metadata endpoint."""
    return jsonify({
        "service": "cloudopshub-aps",
        "redis_connected": bool(os.environ.get('REDIS_URI')),
        "status": "ok"
    }), 200

@app.route('/trigger_process', methods=['POST'])
def trigger_process():
    """Simulated batch processing."""
    time.sleep(random.uniform(0.1, 0.3))
    return jsonify({'message': 'Processed 500 events successfully.'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)