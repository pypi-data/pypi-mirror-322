
import unittest
from ensembleai.agents import Agent
from ensembleai.llm_model import LLMModel

class TestAgent(unittest.TestCase):
    def setUp(self):
        self.model = LLMModel(name="test-model", api_key="test-api-key")
        self.agent = Agent(name="test-agent", model_instance=self.model, role="tester", work="test work")

    def test_agent_initialization(self):
        self.assertEqual(self.agent.name, "test-agent")
        self.assertEqual(self.agent.role, "tester")
        self.assertEqual(self.agent.work, "test work")

    # Add more tests as needed

if __name__ == '__main__':
    unittest.main()
