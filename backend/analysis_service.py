"""
Сервис анализа документов: извлечение текста, вызов OpenAI, сохранение в results.
"""

from backend.document_parser import extract_text
from backend.file_upload import get_document_file_path
from backend.models import Document, Result
from backend.openai_client import complete
from backend.prompts import ANALYSIS_TYPES, get_system_prompt, get_user_content


def run_analysis(document_id: int, analysis_type: str, db) -> Result:
    """
    Запускает анализ документа по типу, сохраняет результат в БД и возвращает его.
    - Загружает Document по document_id, извлекает текст из файла.
    - Подставляет промпт по analysis_type, вызывает OpenAI.
    - Создаёт запись Result и возвращает её.
    Выбрасывает ValueError при неизвестном document_id или analysis_type.
    """
    if analysis_type not in ANALYSIS_TYPES:
        raise ValueError(
            f"Неизвестный тип анализа: {analysis_type}. Допустимы: {list(ANALYSIS_TYPES)}"
        )
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise ValueError(f"Документ с id={document_id} не найден")
    path = get_document_file_path(document)
    if not path.exists():
        raise FileNotFoundError(f"Файл документа не найден: {path}")
    text = extract_text(str(path), document.filename)
    system_prompt = get_system_prompt(analysis_type)
    user_content = get_user_content(text)
    content = complete(system_prompt, user_content)
    result = Result(
        document_id=document_id,
        analysis_type=analysis_type,
        content=content,
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result
