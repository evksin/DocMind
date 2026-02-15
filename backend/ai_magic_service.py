"""
AI Magic: формирует отчёт-консалтинг на основе документа и готовых анализов.
Промпт загружается из docs/AI_MAGIC_PROMPT.md.
"""

from pathlib import Path

from backend.document_parser import extract_text
from backend.file_upload import get_document_file_path
from backend.models import Document, Result
from backend.openai_client import complete

# Путь к мастер-промпту (от корня проекта)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROMPT_PATH = PROJECT_ROOT / "docs" / "AI_MAGIC_PROMPT.md"

# Лимиты длины для входа (укладываемся в лимит токенов OpenRouter)
MAX_DOCUMENT_CHARS = 4_000
MAX_ANALYSIS_CHARS_PER_RESULT = 1_200


def _load_prompt() -> str:
    """Загружает текст промпта из docs/AI_MAGIC_PROMPT.md."""
    if not PROMPT_PATH.exists():
        raise FileNotFoundError(f"Промпт не найден: {PROMPT_PATH}")
    return PROMPT_PATH.read_text(encoding="utf-8").strip()


def _get_document_text(document: Document) -> str:
    """Извлекает текст документа с ограничением длины. Если файла нет — возвращает пояснение."""
    path = get_document_file_path(document)
    if not path.exists():
        return "[Текст документа недоступен — файл не найден (например, после перезапуска сервера). Ниже приведены сохранённые анализы.]"
    try:
        text = extract_text(str(path), document.filename).strip()
    except (FileNotFoundError, OSError):
        return "[Текст документа недоступен. Ниже приведены сохранённые анализы.]"
    if not text:
        return "[Текст документа пуст или не извлечён.]"
    if len(text) > MAX_DOCUMENT_CHARS:
        text = text[:MAX_DOCUMENT_CHARS] + "\n\n[... документ обрезан ...]"
    return text


def _get_structured_analysis(document_id: int, db) -> str:
    """Собирает тексты всех анализов по документу в один блок."""
    results = (
        db.query(Result)
        .filter(Result.document_id == document_id)
        .order_by(Result.created_at.desc())
        .all()
    )
    if not results:
        return "[По документу пока нет сохранённых анализов. Сначала запустите анализ.]"
    parts = []
    for r in results:
        content = (r.content or "").strip()
        if len(content) > MAX_ANALYSIS_CHARS_PER_RESULT:
            content = content[:MAX_ANALYSIS_CHARS_PER_RESULT] + " [...]"
        parts.append(f"--- {r.analysis_type} ---\n{content}")
    return "\n\n".join(parts)


def run_ai_magic(document_id: int, db, audience: str | None = None) -> str:
    """
    Строит AI Magic отчёт: загружает промпт, документ и анализы, вызывает LLM.
    audience: для кого отчёт (business, legal, manager, student) — влияет на тон.
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise ValueError(f"Документ с id={document_id} не найден")

    system_prompt = _load_prompt()
    doc_text = _get_document_text(document)
    analysis_text = _get_structured_analysis(document_id, db)

    user_content = (
        "Original document:\n\n"
        f"{doc_text}\n\n"
        "Structured analysis (extracted by the system):\n\n"
        f"{analysis_text}"
    )
    if audience:
        role_labels = {
            "business": "бизнес",
            "legal": "юридическая",
            "manager": "руководитель",
            "student": "студент",
        }
        label = role_labels.get(audience.lower(), audience)
        user_content = user_content + f"\n\nОтчёт предназначен для аудитории: {label}. Учитывай это в тоне и формулировках."

    return complete(system_prompt, user_content)
