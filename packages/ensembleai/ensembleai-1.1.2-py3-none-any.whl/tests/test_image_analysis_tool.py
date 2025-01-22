
import unittest
from ensembleai.image_analysis_tool import ImageAnalysisTool
from ensembleai.agents import Agent
from ensembleai.llm_model import LLMModel

class TestImageAnalysisTool(unittest.TestCase):
    def setUp(self):
        self.model = LLMModel(name="test-model", api_key="test-api-key")
        self.agent = Agent(name="test-agent", model_instance=self.model, role="tester", work="test work")
        self.tool = ImageAnalysisTool(text="test-text", url="test-url")

    def test_tool_initialization(self):
        self.assertEqual(self.tool.text, "test-text")
        self.assertEqual(self.tool.url, "test-url")

    # Add more tests as needed

if __name__ == '__main__':
    unittest.main()
