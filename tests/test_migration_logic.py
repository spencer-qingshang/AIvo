import unittest
import sys
import os

# Add scripts to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))

from migrate_notes import parse_vocab_table, parse_grammar_list

class TestMigrationLogic(unittest.TestCase):
    def test_parse_vocab_table(self):
        content = "| **apple** | 苹果 | note |\n| **banana** | 香蕉 | |"
        result = parse_vocab_table(content)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['word'], "apple")
        self.assertEqual(result[1]['meaning'], "香蕉")

    def test_parse_grammar_list(self):
        content = "### Rule 1\n- This is a detail"
        result = parse_grammar_list(content)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], "Rule 1")

if __name__ == '__main__':
    unittest.main()
