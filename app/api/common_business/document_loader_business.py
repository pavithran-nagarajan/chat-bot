import os
import chardet
import tempfile
from pypdf import PdfReader
from docx import Document


def extract_text(file_bytes: bytes, filename: str) -> str:
    ext = os.path.splitext(filename)[1].lower()

    if ext == ".pdf":
        return extract_from_pdf(file_bytes)
    elif ext == ".docx":
        return extract_from_docx(file_bytes)
    elif ext == ".txt":
        return extract_from_txt(file_bytes)
    else:
        raise ValueError(f"Unsupported file type: {ext}. Use PDF, DOCX or TXT.")


def extract_from_pdf(file_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name
    try:
        reader = PdfReader(tmp_path)
        pages = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text and text.strip():
                pages.append(f"[Page {i+1}]\n{text.strip()}")
        return "\n\n".join(pages)
    finally:
        os.unlink(tmp_path)


def extract_from_docx(file_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name
    try:
        doc = Document(tmp_path)
        paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        return "\n\n".join(paragraphs)
    finally:
        os.unlink(tmp_path)


def extract_from_txt(file_bytes: bytes) -> str:
    detected = chardet.detect(file_bytes)
    encoding = detected.get("encoding") or "utf-8"
    return file_bytes.decode(encoding, errors="ignore")