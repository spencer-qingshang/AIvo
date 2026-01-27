import re
from pypdf import PdfReader
from collections import Counter

def analyze_vocabulary(pdf_path):
    all_words = []
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
                all_words.extend(words)
        
        unique_words = sorted(list(set(all_words)))
        word_counts = Counter(all_words)
        
        # 获取最常见的单词（基础词）
        common = word_counts.most_common(20)
        
        # 获取长度较长的单词（通常是较难的词）
        long_words = [w for w in unique_words if len(w) > 10][:20]
        
        # 获取一些典型的“初中水平”词汇是否在里面
        basic_check = {word: (word in unique_words) for word in ['apple', 'book', 'good', 'school', 'student', 'happy']}
        
        return len(unique_words), common, long_words, basic_check
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    path = r"G:\\Desktop\\学习\\AIvo\\C1=收集箱\\真题册（校对过的）.pdf"
    count, common, long_words, basic_check = analyze_vocabulary(path)
    print(f"Total Unique Words: {count}")
    print(f"\nMost Common Words (Basic): {common}")
    print(f"\nExample Long Words (Advanced): {long_words}")
    print(f"\nBasic Words Presence: {basic_check}")
