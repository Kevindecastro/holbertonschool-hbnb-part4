import unittest
import json
from app import run

class TestEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = run()
        self.client = self.app.test_client()

    def test_create_user_valid(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)
    
    def test_create_place_valid(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Nice Place",
            "price": 120.50,
            "latitude": 45.76,
            "longitude": 4.85
        })
        self.assertEqual(response.status_code, 201)
    
    def test_create_place_invalid(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "price": -5,
            "latitude": 200,
            "longitude": -190
        })
        self.assertEqual(response.status_code, 400)
    
    def test_create_review_valid(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "user_id": "valid_user_id",
            "place_id": "valid_place_id"
        })
        self.assertEqual(response.status_code, 201)
    
    def test_create_review_invalid(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "user_id": "",
            "place_id": ""
        })
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()