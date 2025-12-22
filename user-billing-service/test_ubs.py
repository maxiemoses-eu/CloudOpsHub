# test_ubs.py
import unittest
import json
from ubs import app, db, User

class UBSTestCase(unittest.TestCase):

    def setUp(self):
        # Configure the app for testing
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Use in-memory DB for tests
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_a_create_user_success(self):
        # Test creation of a new user
        response = self.app.post(
            '/users',
            data=json.dumps({
                'username': 'maxie',
                'email': 'maxie@cloud.com'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['username'], 'maxie')
        self.assertEqual(data['subscription_plan'], 'Free')

    def test_b_get_user_success(self):
        # First create a user
        with app.app_context():
            user = User(username='testuser', email='test@test.com')
            db.session.add(user)
            db.session.commit()
            user_id = user.id

        # Then retrieve the user
        response = self.app.get(f'/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['username'], 'testuser')

    def test_c_health_status(self):
        # Test the health check endpoint
        response = self.app.get('/status')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('status', data)
        # Note: db_connected may be false since we are using in-memory for tests, 
        # but the request itself is successful.

if __name__ == '__main__':
    unittest.main()
