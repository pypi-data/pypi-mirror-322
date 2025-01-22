
import unittest
from ensembleai.tools import Tool

class TestTool(unittest.TestCase):
    def test_tool_use_method(self):
        tool = Tool()
        with self.assertRaises(NotImplementedError):
            tool.use()

    # Add more tests as needed

if __name__ == '__main__':
    unittest.main()
