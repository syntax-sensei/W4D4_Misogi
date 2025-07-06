import pdfplumber
from docx import Document

def extract_text(file_path):
    if file_path.endswith('.pdf'):
        with pdfplumber.open(file_path) as pdf:
            return '\n'.join([page.extract_text() or '' for page in pdf.pages])
    elif file_path.endswith('.docx'):
        doc = Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])
    elif file_path.endswith('.txt'):
        return open(file_path, 'r').read()
    return ""
