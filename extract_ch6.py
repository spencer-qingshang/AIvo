# -*- coding: utf-8 -*-
import re

def extract_chapter_6():
    source_path = 'C1=收集箱/习近平.md'
    output_path = 'temp_ch6.md'
    
    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 尝试找到第六章的标题
    # 假设标题格式类似 "第六章 ..."
    # 前面的章节标题示例： "第五章 全面深化改革开放"
    
    # 查找第六章开始的位置
    match_start = re.search(r'第六章\s+.*', content)
    if not match_start:
        print("未找到第六章")
        return

    start_pos = match_start.start()
    print(f"第六章标题: {match_start.group()}")
    
    # 查找第七章开始的位置
    match_end = re.search(r'第七章\s+.*', content, pos=match_start.end())
    
    if match_end:
        end_pos = match_end.start()
        print(f"第七章标题: {match_end.group()}")
    else:
        end_pos = len(content)
        print("未找到第七章，提取到文件末尾")
        
    ch6_content = content[start_pos:end_pos]
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(ch6_content)
    
    print(f"已提取第六章内容到 {output_path}")

if __name__ == "__main__":
    extract_chapter_6()
