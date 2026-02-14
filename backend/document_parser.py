"""
Извлечение текста из документов: TXT, PDF, DOCX.
"""

from pathlib import Path


def extract_text(file_path: str, filename: str) -> str:
    """
    Извлекает текст из файла по пути. Тип определяется по расширению filename.
    Поддерживаются: .txt, .pdf, .docx (без учёта регистра).
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    ext = Path(filename).suffix.lower()

    if ext == ".txt":
        return _extract_txt(file_path)
    if ext == ".pdf":
        return _extract_pdf(file_path)
    if ext == ".docx":
        return _extract_docx(file_path)

    raise ValueError(f"Неподдерживаемый формат: {ext}. Ожидается .txt, .pdf или .docx")


def _extract_txt(file_path: str) -> str:
    """Чтение TXT в UTF-8 с обработкой ошибок кодировки."""
    with open(file_path, encoding="utf-8", errors="replace") as f:
        return f.read()


def _extract_pdf(file_path: str) -> str:
    """Извлечение текста из PDF через PyMuPDF (fitz)."""
    import fitz  # PyMuPDF

    doc = fitz.open(file_path)
    try:
        parts = []
        for page in doc:
            parts.append(page.get_text())
        return "\n".join(parts)
    finally:
        doc.close()


def _extract_docx(file_path: str) -> str:
    """Извлечение текста из DOCX через python-docx."""
    from docx import Document

    doc = Document(file_path)
    parts = [p.text for p in doc.paragraphs]
    return "\n".join(parts)
