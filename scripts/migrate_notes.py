import os
import re
from datetime import datetime

# 基础路径配置
BASE_PATH = "C4=归档资料/4.1=学习类/4.1.1=英语学习"
TEMPLATE_DIR = os.path.join(BASE_PATH, "模板")
VOCAB_DIR = os.path.join(BASE_PATH, "20=知识库")
REVIEW_DIR = os.path.join(BASE_PATH, "30=复盘")

# 旧文件路径
OLD_NOTES = os.path.join(BASE_PATH, "PETS-3/重点词汇与答疑笔记.md")
OLD_PROGRESS = os.path.join(BASE_PATH, "美剧/摩登家庭/每日学习进度表.md")

def load_template(name):
    path = os.path.join(TEMPLATE_DIR, f"{name}模板.md")
    if not os.path.exists(path):
        return ""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def parse_vocab_table(content):
    """从 Markdown 内容中解析词汇表格"""
    # 匹配表格行 | Word | Meaning | Note |
    pattern = r"\|\s*\*\*([^*]+)\*\*\s*\|\s*([^|]+)\s*\|\s*([^|]*)\s*\|"
    matches = re.findall(pattern, content)
    return [{"word": m[0].strip(), "meaning": m[1].strip(), "note": m[2].strip()} for m in matches]

def parse_grammar_list(content):
    """解析以 ### 标题开头的语法/错题列表"""
    # 匹配 ### 标题和随后的列表项
    pattern = r"### ([^\n]+)\n- ([^\n]+)"
    matches = re.findall(pattern, content)
    return [{"title": m[0].strip(), "detail": m[1].strip()} for m in matches]

def parse_progress_table(content):
    """从进度表中解析行"""
    pattern = r"\|\s*\*\*(\d{4}-\d{2}-\d{2})\*\*\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|"
    matches = re.findall(pattern, content)
    return [{"date": m[0], "range": m[1].strip(), "phase": m[2].strip(), "status": m[3].strip(), "summary": m[4].strip()} for m in matches]

def generate_review_note(prog, template):
    """生成每日复盘笔记"""
    content = template.replace("{{date}}", prog['date'])
    content = content.replace("0 # 1-10", "10") # 默认满分
    content = content.replace("- **完成任务**: ", f"- **完成任务**: {prog['range']}")
    content = content.replace("- **学习时长**: ", f"- **学习时长**: {prog['phase']}")
    content = content.replace("## 闪光点\n- ", f"## 闪光点\n- {prog['summary']}")
    
    filename = f"复盘_{prog['date']}.md"
    filepath = os.path.join(REVIEW_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created review note: {filename}")

def generate_error_note(err, template):
    """生成错题笔记"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    content = template.replace("{{date}}", date_str)
    content = content.replace("# Error Log: {{date}}", f"# 错题记录: {err['title']}")
    content = content.replace("- **正确写法**: ", f"- **正确写法**: {err['detail']}")
    
    # 清理文件名
    safe_title = re.sub(r'[\\/*?:":<>|]', "", err['title'])
    filename = f"错题_{safe_title}.md"
    filepath = os.path.join(REVIEW_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created error note: {filename}")

def generate_vocab_note(vocab, template):
    """生成单词笔记"""
    content = template.replace("{{title}}", vocab['word'])
    content = content.replace("{{date}}", datetime.now().strftime("%Y-%m-%d"))
    
    # 填充释义
    content = content.replace("- \n", f"- {vocab['meaning']}\n", 1)
    
    filename = f"{vocab['word']}.md"
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)
    filepath = os.path.join(VOCAB_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created vocab note: {filename}")

def main():
    # 确保目录存在
    os.makedirs(VOCAB_DIR, exist_ok=True)
    os.makedirs(REVIEW_DIR, exist_ok=True)

    # 1. 迁移单词
    if os.path.exists(OLD_NOTES):
        with open(OLD_NOTES, 'r', encoding='utf-8') as f:
            old_content = f.read()
        
        # 提取单词
        vocabs = parse_vocab_table(old_content)
        vocab_template = load_template("单词")
        for v in vocabs:
            generate_vocab_note(v, vocab_template)
            
        # 提取语法/错题
        errors = parse_grammar_list(old_content)
        error_template = load_template("错题")
        for e in errors:
            generate_error_note(e, error_template)

    # 2. 迁移进度
    if os.path.exists(OLD_PROGRESS):
        with open(OLD_PROGRESS, 'r', encoding='utf-8') as f:
            prog_content = f.read()
        
        progress_entries = parse_progress_table(prog_content)
        review_template = load_template("复盘")
        for p in progress_entries:
            generate_review_note(p, review_template)

    print("Migration finished.")

if __name__ == "__main__":
    main()
