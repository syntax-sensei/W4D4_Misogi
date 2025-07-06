import re

def chunk_text(text, max_tokens=300):
    paragraphs = text.split("\n\n")
    chunks, current = [], ""
    for para in paragraphs:
        if len(current.split()) + len(para.split()) <= max_tokens:
            current += "\n" + para
        else:
            chunks.append(current.strip())
            current = para
    if current:
        chunks.append(current.strip())
    return chunks
