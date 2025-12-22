# test_aps.py
import unittest
import json
from aps import app

class APSTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_status_endpoint(self):
        response = self.app.get('/status')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('processing_target', data)

    def test_trigger_process_endpoint(self):
        # We test that the endpoint executes successfully, though the processing is mocked
        response = self.app.post('/trigger_process')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('triggered successfully', data['message'])

if __name__ == '__main__':
    unittest.main()
