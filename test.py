import unittest
from app import app
import json
import os


class TestApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        if os.path.exists("data/test_todolist.yaml"):
            os.remove("data/test_todolist.yaml")

    def test_new_and_getall(self):
        data = {'date': '2024-03-20', 'name': 'Faire les courses', 'description': 'Acheter du lait, du pain, et des œufs'}
        response = self.app.post('/new', json=data)
        self.assertEqual(response.status_code, 204)
        
        response = self.app.get('/getall')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIn(b'Faire les courses', response.data)

    
    def test_healthz(self):
        response = self.app.get('/healthz')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data), {"status": "OK"})

    def test_readiness(self):
        response = self.app.get('/readiness')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data), {"status": "OK"})


if __name__ == '__main__':
    unittest.main()
