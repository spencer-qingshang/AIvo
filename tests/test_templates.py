import os
import unittest

class TestTemplates(unittest.TestCase):
    def test_source_note_template_content(self):
        template_path = "Templates/Source Note.md"
        self.assertTrue(os.path.exists(template_path), "Templates/Source Note.md should exist")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("type: source", content)
            self.assertIn("status: ", content)
            self.assertIn("tags: ", content)
            self.assertIn("level: ", content)

    def test_vocab_note_template_content(self):
        template_path = "Templates/Vocab Note.md"
        self.assertTrue(os.path.exists(template_path), "Templates/Vocab Note.md should exist")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("type: vocab", content)
            self.assertIn("definitions: ", content)
            self.assertIn("examples: ", content)
            self.assertIn("mastery: ", content)

    def test_grammar_note_template_content(self):
        template_path = "Templates/Grammar Note.md"
        self.assertTrue(os.path.exists(template_path), "Templates/Grammar Note.md should exist")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("type: grammar", content)
            self.assertIn("difficulty: ", content)

    def test_error_log_template_content(self):
        template_path = "Templates/Error Log.md"
        self.assertTrue(os.path.exists(template_path), "Templates/Error Log.md should exist")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("type: error", content)
            self.assertIn("reason: ", content)
            self.assertIn("related_source: ", content)

    def test_daily_review_template_content(self):
        template_path = "Templates/Daily Review.md"
        self.assertTrue(os.path.exists(template_path), "Templates/Daily Review.md should exist")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("type: review", content)
            self.assertIn("date: ", content)
            self.assertIn("score: ", content)

if __name__ == '__main__':
    unittest.main()
