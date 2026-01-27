import re
from pypdf import PdfReader

def count_unique_words(pdf_path):
    unique_words = set()
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                # 提取英文单词并转为小写
                words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
                unique_words.update(words)
        return len(unique_words)
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    path = r"G:\Desktop\学习\AIvo\C1=收集箱\真题册（校对过的）.pdf"
    result = count_unique_words(path)
    print(f"Unique words count: {result}")
