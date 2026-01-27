#!/usr/bin/env python3
"""
Log Error Script for English Study Helper
Appends learning errors to the daily feedback log.
"""

import argparse
import os
import datetime
import re

# Configuration
BASE_DIR = r"C4=归档资料\4.1=学习类\4.1.1=英语学习\美剧\摩登家庭"
LOG_FILE = os.path.join(BASE_DIR, "练习反馈日志.md")

def main():
    parser = argparse.ArgumentParser(description="Log Learning Error")
    parser.add_argument("--content", required=True, help="Content of the error")
    parser.add_argument("--type", default="拼写", help="Type of error (拼写/语法/听力)")
    
    args = parser.parse_args()
    
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    header = f"## 📅 {today_str}"
    
    # Check if file exists
    if not os.path.exists(LOG_FILE):
        print(f"❌ Log file not found: {LOG_FILE}")
        return

    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    new_entry = f"    - [ ] **[{args.type}]** {args.content}\n"

    # Strategy: 
    # 1. Look for today's header.
    # 2. If found, append entry under it.
    # 3. If not found, append new header and entry at the end.

    if header in content:
        # Simple append isn't enough if we want it *under* the header inside the file.
        # But for robustness in v1, appending at the end is safest if header is last.
        # However, to be smarter, let's just append to the end of file if header exists, 
        # assuming the user is working on the latest entry.
        # Better strategy: Replace the whole file content inserting the line.
        
        # Find the index of the header
        # We will simply append to the file, but we need to ensure we are in the right section.
        # If the file ends with today's section, appending is fine.
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
             f.write(new_entry)
        print(f"✅ Appended to existing section for {today_str}")
        
    else:
        # Create new section
        new_section = f"\n\n{header}\n- **自动记录：**\n{new_entry}"
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(new_section)
        print(f"✅ Created new section for {today_str}")

if __name__ == "__main__":
    main()
