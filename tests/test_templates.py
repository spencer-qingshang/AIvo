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

if __name__ == '__main__':
    unittest.main()
