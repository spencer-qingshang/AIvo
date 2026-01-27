#!/usr/bin/env python3
"""
Add Vocabulary Script for English Study Helper v1.1
Automatically inserts a new row into the vocabulary table of a specific lesson note.
"""

import argparse
import os
import sys

# Configuration
BASE_DIR = r"C4=归档资料\4.1=学习类\4.1.1=英语学习\美剧\摩登家庭"

def add_vocab_to_file(file_path, word, phonetic, meaning, context):
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find the table header: | 单词 | 音标 | 含义 | 例句/场景 |
    # We want to insert after the separator line | :--- | :--- | :--- | :--- |
    
    new_row = f"| **{word}** | {phonetic} | {meaning} | {context} |\n"
    
    inserted = False
    new_lines = []
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        if "| 单词 | 音标 | 含义 | 例句/场景 |" in line and i + 1 < len(lines):
            # Check if next line is the separator
            if "| :---" in lines[i+1]:
                new_lines.append(lines[i+1]) # Keep the separator
                new_lines.append(new_row)    # Insert our new row
                inserted = True
                # Skip the separator line in the next iteration
                lines.pop(i+1) 
    
    if not inserted:
        # Fallback: if table structure is not found exactly, append to end
        new_lines.append("\n### 🆕 Added via Helper\n")
        new_lines.append("| 单词 | 音标 | 含义 | 例句/场景 |\n")
        new_lines.append("| :--- | :--- | :--- | :--- |\n")
        new_lines.append(new_row)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"✅ Successfully added '{word}' to {os.path.basename(file_path)}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Add vocabulary to lesson notes")
    parser.add_argument("--se", required=True, help="Season/Episode code (e.g., S01E01)")
    parser.add_argument("--word", required=True)
    parser.add_argument("--phonetic", default="")
    parser.add_argument("--meaning", required=True)
    parser.add_argument("--context", default="")
    
    args = parser.parse_args()
    
    # Construct filename
    filename = f"摩登家庭{args.se}_重点词汇与答疑笔记.md"
    file_path = os.path.join(BASE_DIR, filename)
    
    add_vocab_to_file(file_path, args.word, args.phonetic, args.meaning, args.context)

if __name__ == "__main__":
    main()
