import unittest

from src.api import create_app


class TestAPI(unittest.TestCase):
    def setUp(self):
        app = create_app()
        self.client = app.test_client()

    def test_create_transaction(self):
        response = self.client.post(
            "/transaction",
            json={
                "date": "2021-01-01",
                "amount": 100,
                "description": "test",
                "tags": ["test"],
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json,
            {
                "id": "1",
                "date": "2021-01-01",
                "amount": 100,
                "description": "test",
                "tags": ["test"],
            },
        )

    def test_addition(self):
        response = self.client.get("/add?x=2&y=3")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"5")
