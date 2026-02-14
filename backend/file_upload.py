"""
Сохранение загруженных файлов на диск и запись в БД.
Шаг 3.2: каталог загрузок, сохранение файла, связь с пользователем в БД.
"""

import re
import uuid
from pathlib import Path

from backend.database import BASE_DIR
from backend.models import Document

# Каталог для загрузок: backend/uploads/
UPLOADS_DIR = BASE_DIR / "uploads"


def ensure_uploads_dir() -> Path:
    """Создаёт каталог uploads, если его нет. Возвращает путь к каталогу."""
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    return UPLOADS_DIR


def _sanitize_filename(name: str) -> str:
    """Оставляет в имени файла только безопасные символы."""
    name = re.sub(r"[^\w\s\-\.]", "", name)
    return name.strip() or "document"


def save_upload(
    file_content: bytes,
    filename: str,
    user_id: int,
    db,
) -> Document:
    """
    Сохраняет загруженный файл на диск и создаёт запись Document в БД.
    Имя файла на диске: uuid_оригинальное_имя для уникальности.
    Возвращает созданный объект Document.
    """
    ensure_uploads_dir()
    safe_name = _sanitize_filename(filename)
    unique_name = f"{uuid.uuid4().hex}_{safe_name}"
    file_path = UPLOADS_DIR / unique_name
    file_path.write_bytes(file_content)
    # В БД храним относительный путь от backend: uploads/имя
    path_for_db = f"uploads/{unique_name}"
    doc = Document(
        user_id=user_id,
        filename=filename,
        file_path=path_for_db,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def get_document_file_path(document: Document) -> Path:
    """Возвращает полный путь к файлу на диске по записи Document."""
    return BASE_DIR / document.file_path


def delete_document_file(document: Document) -> None:
    """Удаляет файл документа с диска. Не выбрасывает ошибку, если файла нет."""
    path = get_document_file_path(document)
    if path.exists():
        try:
            path.unlink()
        except OSError:
            pass
