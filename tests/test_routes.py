import unittest
from app.nlp.processing import generate_response, tokenizer, model
from tests.rich_test_result import RichTestRunner

class TestChatbot(unittest.TestCase):
    def setUp(self):
        """
        Set up resources for testing, including the tokenizer and model.
        """
        self.tokenizer = tokenizer
        self.model = model

    def test_generate_response_basic(self):
        """
        Test a basic user input and response generation.
        """
        user_input = "What is the capital of France?"
        response, chat_history = generate_response(user_input)

        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_generate_response_empty_input(self):
        """
        Test the behavior when given an empty input.
        """
        user_input = ""
        response, chat_history = generate_response(user_input)
        self.assertIsInstance(response, str)

    def test_generate_response_long_input(self):
        """
        Test the behavior when given a very long input.
        """
        user_input = "Hello " * 1000  # Simulate a long input
        response, chat_history = generate_response(user_input)

        self.assertIsInstance(response, str)
        self.assertLessEqual(len(response), 1000)  # Response should respect max_length

    def test_generate_response_with_history(self):
        """
        Test response generation with chat history.
        """
        user_input1 = "What is your name?"
        user_input2 = "How old are you?"
        _, chat_history = generate_response(user_input1)
        response, chat_history = generate_response(user_input2, chat_history)

        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_generate_response_error_handling(self):
        """
        Test if the function handles exceptions gracefully.
        """
        user_input = None  # Invalid input
        response, chat_history = generate_response(user_input)

        self.assertIsInstance(response, str)
        self.assertTrue(response.startswith("Error"))

if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner())