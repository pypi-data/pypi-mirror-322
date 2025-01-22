
import unittest
from ensembleai.wikipedia_tool import WikipediaTool
from ensembleai.agents import Agent
from ensembleai.llm_model import LLMModel

class TestWikipediaTool(unittest.TestCase):
    def setUp(self):
        self.model = LLMModel(name="test-model", api_key="test-api-key")
        self.agent = Agent(name="test-agent", model_instance=self.model, role="tester", work="test work")
        self.tool = WikipediaTool(topic="test-topic")

    def test_tool_initialization(self):
        self.assertEqual(self.tool.topic, "test-topic")

    # Add more tests as needed

if __name__ == '__main__':
    unittest.main()
