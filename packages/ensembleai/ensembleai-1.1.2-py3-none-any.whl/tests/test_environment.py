
import unittest
from ensembleai.environment import Environment
from ensembleai.agents import Agent
from ensembleai.llm_model import LLMModel

class TestEnvironment(unittest.TestCase):
    def setUp(self):
        self.model = LLMModel(name="test-model", api_key="test-api-key")
        self.agent = Agent(name="test-agent", model_instance=self.model, role="tester", work="test work")
        self.env = Environment(agents=[self.agent])

    def test_environment_initialization(self):
        self.assertEqual(len(self.env.agents), 1)

    # Add more tests as needed

if __name__ == '__main__':
    unittest.main()
