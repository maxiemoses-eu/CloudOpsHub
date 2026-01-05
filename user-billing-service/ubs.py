from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuration aligned with Helm Secrets/ConfigMaps
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///test_ubs.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    subscription_plan = db.Column(db.String(50), default='Free')
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'subscription_plan': self.subscription_plan
        }

# --- Standardized Health Endpoints ---

@app.route('/health', methods=['GET'])
def health():
    """Liveness Probe: Service is alive"""
    return jsonify({'status': 'alive'}), 200

@app.route('/ready', methods=['GET'])
def ready():
    """Readiness Probe: Check Database Connectivity"""
    try:
        db.session.execute(db.text('SELECT 1'))
        return jsonify({'status': 'ready', 'db_connected': True}), 200
    except Exception:
        return jsonify({'status': 'not_ready', 'db_connected': False}), 503

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'OK'}), 200

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if not data or 'username' not in data or 'email' not in data:
        return jsonify({'message': 'Missing required fields'}), 400
    new_user = User(username=data['username'], email=data['email'])
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)