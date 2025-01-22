
import unittest
from ensembleai.llm_model import LLMModel

class TestLLMModel(unittest.TestCase):
    def setUp(self):
        self.model = LLMModel(name="test-model", api_key="test-api-key")

    def test_model_initialization(self):
        self.assertEqual(self.model.name, "test-model")
        self.assertEqual(self.model.api_key, "test-api-key")

    # Add more tests as needed

if __name__ == '__main__':
    unittest.main()
