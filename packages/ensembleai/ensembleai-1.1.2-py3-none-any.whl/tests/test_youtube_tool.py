
import unittest
from ensembleai.youtube_tool import YouTubeTranscriptTool
from ensembleai.agents import Agent
from ensembleai.llm_model import LLMModel

class TestYouTubeTranscriptTool(unittest.TestCase):
    def setUp(self):
        self.model = LLMModel(name="test-model", api_key="test-api-key")
        self.agent = Agent(name="test-agent", model_instance=self.model, role="tester", work="test work")
        self.tool = YouTubeTranscriptTool(api_key="test-api-key", keyword="test-keyword")

    def test_tool_initialization(self):
        self.assertEqual(self.tool.api_key, "test-api-key")
        self.assertEqual(self.tool.keyword, "test-keyword")

    # Add more tests as needed

if __name__ == '__main__':
    unittest.main()
