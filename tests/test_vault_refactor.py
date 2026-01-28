import os
import unittest

class TestVaultStructure(unittest.TestCase):
    base_path = "C4=归档资料/4.1=学习类/4.1.1=英语学习"
    
    def test_directories_exist(self):
        required_dirs = [
            "00=仪表盘",
            "10=学习素材",
            "20=知识库",
            "30=复盘",
            "40=考试",
            "99=归档",
            "模板"
        ]
        
        for d in required_dirs:
            full_path = os.path.join(self.base_path, d)
            self.assertTrue(os.path.exists(full_path), f"目录 {full_path} 应该存在")

    def test_templates_exist(self):
        required_templates = [
            "素材模板.md",
            "单词模板.md",
            "语法模板.md",
            "错题模板.md",
            "复盘模板.md"
        ]
        
        for t in required_templates:
            full_path = os.path.join(self.base_path, "模板", t)
            self.assertTrue(os.path.exists(full_path), f"模板文件 {full_path} 应该存在")

if __name__ == '__main__':
    unittest.main()
