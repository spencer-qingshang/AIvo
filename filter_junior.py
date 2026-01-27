import re
import ssl
import urllib.request
from pypdf import PdfReader

def get_online_common_words():
    """
    下载 Google 的 10000 个最常用英语单词列表（按频率排序）。
    我们将取前 2000 个作为'初中/基础水平'的近似值。
    """
    url = "https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-usa-no-swears.txt"
    try:
        # 忽略 SSL 证书验证以避免环境问题
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(url, context=context, timeout=10) as response:
            content = response.read().decode('utf-8')
            # 获取前 2000 个词
            words = content.splitlines()[:2000]
            return set(words)
    except Exception as e:
        print(f"Warning: Could not download online list ({e}). Using heuristic fallback.")
        return set()

def analyze_net_vocabulary(pdf_path):
    # 1. 提取 PDF 单词
    pdf_words = set()
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                # 简单清洗：只保留纯字母，转小写
                words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
                pdf_words.update(words)
    except Exception as e:
        return f"Error reading PDF: {e}"

    print(f"Total unique words in PDF: {len(pdf_words)}")

    # 2. 获取基础词汇表 (模拟初中水平)
    basic_words = get_online_common_words()
    
    if not basic_words:
        # 如果下载失败，使用备用方案（这里仅作演示，实际上如果没网会比较难精准）
        # 但我们假设下载会成功
        print("Using empty basic list (Download failed).")
        return

    print(f"Basic vocabulary reference size: {len(basic_words)}")

    # 3. 剔除基础词
    advanced_words = pdf_words - basic_words
    
    # 4. 分析结果
    print(f"-" * 30)
    print(f"Words remaining after removing Top 2000 common words: {len(advanced_words)}")
    print(f"-" * 30)
    
    # 展示一些被剔除的词（验证准确性）
    removed = list(pdf_words.intersection(basic_words))[:10]
    print(f"Examples of removed (Basic) words: {removed}")
    
    # 展示剩下的词（即您需要背的）
    remaining = sorted(list(advanced_words))
    print(f"Examples of remaining (Advanced) words: {remaining[500:520]}") # 随机取中间一段

if __name__ == "__main__":
    path = r"G:\Desktop\学习\AIvo\C1=收集箱\真题册（校对过的）.pdf"
    analyze_net_vocabulary(path)
