import os
import unittest

class TestDynamicViews(unittest.TestCase):
    def test_mistake_bank_exists(self):
        file_path = "C4=归档资料/4.1=学习类/4.1.1=英语学习/30=复盘/错题库.md"
        self.assertTrue(os.path.exists(file_path), f"File {file_path} should exist")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("```dataview", content)

    def test_vocab_book_exists(self):
        file_path = "C4=归档资料/4.1=学习类/4.1.1=英语学习/20=知识库/生词本.md"
        self.assertTrue(os.path.exists(file_path), f"File {file_path} should exist")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("```dataview", content)

if __name__ == '__main__':
    unittest.main()