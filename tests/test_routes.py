import unittest
from app import create_app

class ChatbotRouteTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_chat_route_valid_input(self):
        response = self.client.post('/chat', json={"message": "Hello, how are you?"})
        self.assertEqual(response.status_code, 200)
        json_response = response.get_json()
        self.assertIn("chatbot_name", json_response)
        self.assertIn("welcome_message", json_response)
        self.assertIn("response", json_response)

    def test_chat_route_no_input(self):
        response = self.client.post('/chat', json={})
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
