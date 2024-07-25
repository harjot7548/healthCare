# Initialize the test module
import unittest
from app import create_app

class BasicTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Welcome to the HealthCare Backend API!")

if __name__ == '__main__':
    unittest.main()
