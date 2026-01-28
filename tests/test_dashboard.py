import os
import unittest

class TestDashboard(unittest.TestCase):
    def test_dashboard_exists_and_has_queries(self):
        dashboard_path = "C4=归档资料/4.1=学习类/4.1.1=英语学习/00=仪表盘/英语学习主页.md"
        self.assertTrue(os.path.exists(dashboard_path), f"Dashboard file {dashboard_path} should exist")
        
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("## 🚀 当前活跃任务", content)
            self.assertIn("## 💡 待复习知识点", content)
            self.assertIn("## 📈 学习统计", content)
            self.assertIn("```dataviewjs", content)

if __name__ == '__main__':
    unittest.main()
