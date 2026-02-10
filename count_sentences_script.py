import re

def count_sentences(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    total_sentences = 0
    for line in lines:
        if not line.strip():
            continue
        
        # Split timestamp and dialogue
        parts = line.split('	', 1)
        if len(parts) < 2:
            continue
        
        dialogue = parts[1]
        
        # Remove stage directions like (BOTH CHUCKLE)
        dialogue = re.sub(r'\(.*?\)', '', dialogue)
        
        # Handle names like CLAIRE: Kids!
        if ':' in dialogue and dialogue.split(':', 1)[0].isupper():
            dialogue = dialogue.split(':', 1)[1]
        
        # Clean up
        dialogue = dialogue.strip()
        if not dialogue:
            continue
            
        # Count sentences by splitting on typical marks
        # Treating ... and … as sentence breaks if they are used as such
        dialogue = dialogue.replace('…', '.').replace('...', '.')
        
        # Split by . ! ?
        sentences = re.split(r'[.!?]+', dialogue)
        # Filter out empty or whitespace-only results
        valid_sentences = [s.strip() for s in sentences if s.strip()]
        total_sentences += len(valid_sentences)
        
    return total_sentences

if __name__ == "__main__":
    path = r'C4=归档资料/4.1=学习类/4.1.1=英语学习/美剧/摩登家庭/S101.md'
    print(count_sentences(path))
