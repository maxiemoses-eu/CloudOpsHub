import unittest
import json
from aps import app

class APSTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_health_path(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)

    def test_ready_path(self):
        response = self.client.get('/ready')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()