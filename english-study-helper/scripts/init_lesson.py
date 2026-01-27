#!/usr/bin/env python3
"""
Initialize Lesson Script for English Study Helper
Creates standard note files for a new Modern Family episode.
"""

import argparse
import os
import datetime
import sys

# Configuration: Relative paths from Project Root
BASE_DIR = r"C4=归档资料\4.1=学习类\4.1.1=英语学习\美剧\摩登家庭"
PROGRESS_FILE = os.path.join(BASE_DIR, "每日学习进度表.md")

def create_file(path, content):
    if os.path.exists(path):
        print(f"⚠️  File already exists: {path}")
        return False
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Created: {path}")
    return True

def append_to_progress(season, episode):
    today = datetime.date.today().strftime("%Y-%m-%d")
    # Determine next day for review
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    
    entry_lines = [
        f"| **{today}** | {season}{episode} (Part 1) | 🟢 初学 | [ ] | (待听写) |",
        f"| **{tomorrow}** | {season}{episode} (Part 1) | 🟡 复习 | [ ] | (待回译) |"
    ]
    
    if not os.path.exists(PROGRESS_FILE):
        print(f"❌ Progress file not found: {PROGRESS_FILE}")
        return

    with open(PROGRESS_FILE, 'a', encoding='utf-8') as f:
        f.write("\n" + "\n".join(entry_lines))
    print(f"✅ Updated Progress Table: {PROGRESS_FILE}")

def main():
    parser = argparse.ArgumentParser(description="Initialize English Lesson Files")
    parser.add_argument("--season", required=True, help="Season number (e.g., 01)")
    parser.add_argument("--episode", required=True, help="Episode number (e.g., 02)")
    
    args = parser.parse_args()
    
    # Format: S01E02
    se_code = f"S{args.season}E{args.episode}"
    chinese_name = f"摩登家庭{se_code}"
    
    # 1. Create Vocab Note
    vocab_path = os.path.join(BASE_DIR, f"{chinese_name}_重点词汇与答疑笔记.md")
    vocab_content = f"""# {chinese_name} 重点词汇与答疑笔记

> [!abstract] 剧情简介
> (待补充)

## 📝 核心词汇 (New Words)
| 单词 | 音标 | 含义 | 例句/场景 |
| :--- | :--- | :--- | :--- |
|      |      |      |      |

## 💬 口语金句 (Expressions)
- 

## 语法分析 (Grammar)
- 
"""
    create_file(vocab_path, vocab_content)
    
    # 2. Create Back-Translation List
    bt_path = os.path.join(BASE_DIR, f"{chinese_name}_回译练习清单.md")
    bt_content = f"""# {chinese_name} 回译练习清单

## 📅 Part 1 (1-50句)
1. 
2. 
3. 

## 📅 Part 2 (51-100句)
"""
    create_file(bt_path, bt_content)
    
    # 3. Update Progress Table
    append_to_progress(f"S{args.season}", f"E{args.episode}")

if __name__ == "__main__":
    main()
