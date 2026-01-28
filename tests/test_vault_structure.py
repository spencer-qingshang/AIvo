import os
import unittest

class TestDirectoryStructure(unittest.TestCase):
    def test_directories_exist(self):
        required_dirs = [
            "00_Dashboard",
            "10_Inputs",
            "20_Knowledge",
            "30_Review",
            "40_Exam",
            "99_Archive",
            "Templates"
        ]
        
        for d in required_dirs:
            self.assertTrue(os.path.exists(d), f"Directory {d} should exist")

if __name__ == '__main__':
    unittest.main()
