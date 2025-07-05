import fitz  # PyMuPDF
import docx
import os

def extract_text_from_pdf(path):
    doc = fitz.open(path)
    return "\n".join(page.get_text() for page in doc)

def extract_text_from_docx(path):
    doc = docx.Document(path)
    return "\n".join(p.text for p in doc.paragraphs)

def extract_text(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(path)
    elif ext == ".docx":
        return extract_text_from_docx(path)
    elif ext == ".txt":
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError("Unsupported file type")
