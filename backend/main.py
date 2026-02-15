"""
DocMind — минимальный FastAPI backend.
Фаза 1–2: health-check, БД. Фаза 5: API. Фаза 8: CORS и статика.
"""

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from datetime import datetime

logger = logging.getLogger(__name__)

from fastapi import Depends, File, FastAPI, HTTPException, UploadFile
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse, Response
from starlette.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.ai_magic_service import run_ai_magic
from backend.analysis_service import run_analysis
from backend.demo_document import DEMO_FILENAME, get_demo_pdf_bytes
from backend.database import Base, SessionLocal, engine, get_db
from backend import models  # регистрация моделей у Base
from backend.file_upload import delete_document_file, ensure_uploads_dir, save_upload
from backend.report_pdf import report_text_to_pdf


# --- Схемы запросов/ответов ---


class LoginRequest(BaseModel):
    """Тело POST /api/login."""

    username: str = Field(..., min_length=1, max_length=255, description="Имя пользователя")


class LoginResponse(BaseModel):
    """Ответ после логина."""

    user_id: int
    username: str


class DocumentListItem(BaseModel):
    """Элемент списка документов пользователя."""

    id: int
    filename: str
    uploaded_at: datetime


class DocumentUploadResponse(BaseModel):
    """Ответ после загрузки документа."""

    document_id: int


class AnalyzeRequest(BaseModel):
    """Тело POST /api/analyze."""

    document_id: int
    analysis_type: str = Field(
        ...,
        description="summary | action_items | risks | explain_simple",
    )
    user_id: int | None = None
    audience: str | None = Field(None, description="business | legal | manager | student")


class AnalyzeResponse(BaseModel):
    """Ответ после запуска анализа."""

    result_id: int
    content: str


class ResultListItem(BaseModel):
    """Элемент списка результатов по документу."""

    id: int
    document_id: int
    analysis_type: str
    content: str
    created_at: datetime


class ResultDetailResponse(BaseModel):
    """Полный результат по id (GET /api/results/{result_id})."""

    id: int
    document_id: int
    analysis_type: str
    content: str
    created_at: datetime


class AIMagicRequest(BaseModel):
    """Тело POST /api/ai-magic."""

    document_id: int
    audience: str | None = Field(None, description="business | legal | manager | student")


class AIMagicResponse(BaseModel):
    """Ответ AI Magic — консалтинговый отчёт."""

    report: str


class ExportReportRequest(BaseModel):
    """Тело POST /api/export-report — текст отчёта для экспорта в PDF."""

    report_text: str = Field(..., description="Текст AI Magic отчёта")


class DemoRunRequest(BaseModel):
    """Тело POST /api/demo/run."""

    user_id: int


class DemoRunResponse(BaseModel):
    """Ответ демо-режима: document_id и result_id для редиректа на результат."""

    document_id: int
    result_id: int


@asynccontextmanager
async def lifespan(app: FastAPI):
    """При старте приложения создаём таблицы в БД и каталог для загрузок."""
    Base.metadata.create_all(bind=engine)
    ensure_uploads_dir()
    yield
    # при завершении ничего не делаем


app = FastAPI(title="DocMind", version="0.1.0", lifespan=lifespan)

# CORS для фронтенда (localhost / 127.0.0.1, типичные порты)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:8001",
        "http://127.0.0.1:8001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    """Проверка доступности сервера."""
    return {"status": "ok"}


@app.post("/api/login", response_model=LoginResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    """
    Простой «логин» без пароля: по имени пользователя вернуть user_id и username.
    Если пользователь с таким именем есть — возвращаем его; иначе создаём нового.
    """
    from backend.models import User

    username = body.username.strip()
    if not username:
        raise HTTPException(status_code=400, detail="Имя пользователя не может быть пустым")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        user = User(username=username)
        db.add(user)
        db.commit()
        db.refresh(user)
    return LoginResponse(user_id=user.id, username=user.username)


# Допустимые расширения для загрузки документов
ALLOWED_EXTENSIONS = {".txt", ".pdf", ".docx"}


@app.get("/api/users/{user_id}/documents", response_model=list[DocumentListItem])
def list_documents(user_id: int, db: Session = Depends(get_db)):
    """Список документов пользователя: id, filename, uploaded_at."""
    from backend.models import Document, User

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    docs = db.query(Document).filter(Document.user_id == user_id).order_by(Document.uploaded_at.desc()).all()
    return [DocumentListItem(id=d.id, filename=d.filename, uploaded_at=d.uploaded_at) for d in docs]


@app.get("/api/users/{user_id}/documents/{document_id}", response_model=DocumentListItem)
def get_document(user_id: int, document_id: int, db: Session = Depends(get_db)):
    """Один документ пользователя (для страницы анализа)."""
    from backend.models import Document, User

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    doc = db.query(Document).filter(Document.id == document_id, Document.user_id == user_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Документ не найден")
    return DocumentListItem(id=doc.id, filename=doc.filename, uploaded_at=doc.uploaded_at)


@app.post("/api/users/{user_id}/documents", response_model=DocumentUploadResponse)
def upload_document(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Загрузка файла (PDF, TXT, DOCX): сохранение на диск, запись в БД, возврат document_id."""
    from backend.models import User

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if not file.filename:
        raise HTTPException(status_code=400, detail="Имя файла отсутствует")
    ext = "." + file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Недопустимый формат. Разрешены: {', '.join(ALLOWED_EXTENSIONS)}",
        )
    try:
        content = file.file.read()
        doc = save_upload(content, file.filename, user_id, db)
        return DocumentUploadResponse(document_id=doc.id)
    except OSError as e:
        logger.exception("Ошибка записи файла при загрузке")
        raise HTTPException(
            status_code=507,
            detail="Не удалось сохранить файл (диск или права доступа). Попробуйте позже.",
        )
    except Exception as e:
        logger.exception("Ошибка при загрузке документа")
        raise HTTPException(
            status_code=500,
            detail="Ошибка при сохранении документа. Попробуйте позже.",
        )


@app.post("/api/users/{user_id}/documents/{document_id}/delete")
def delete_document(user_id: int, document_id: int, db: Session = Depends(get_db)):
    """Удаление документа: файл с диска, результаты и запись в БД. POST для совместимости."""
    from backend.models import Document, Result, User

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    doc = db.query(Document).filter(Document.id == document_id, Document.user_id == user_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Документ не найден")
    try:
        db.query(Result).filter(Result.document_id == document_id).delete()
        db.delete(doc)
        db.commit()
        delete_document_file(doc)
    except Exception as e:
        db.rollback()
        logger.exception("Ошибка при удалении документа")
        raise HTTPException(status_code=500, detail="Не удалось удалить документ.")
    return {"status": "ok"}


@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze(body: AnalyzeRequest, db: Session = Depends(get_db)):
    """
    Запуск анализа документа: извлечение текста, вызов OpenAI, сохранение в results.
    Возвращает result_id и content. Если передан user_id — проверяется владение документом.
    """
    if body.user_id is not None:
        from backend.models import Document

        doc = db.query(Document).filter(
            Document.id == body.document_id,
            Document.user_id == body.user_id,
        ).first()
        if not doc:
            raise HTTPException(status_code=404, detail="Документ не найден")
    try:
        result = run_analysis(body.document_id, body.analysis_type, db, audience=body.audience)
        return AnalyzeResponse(result_id=result.id, content=result.content)
    except ValueError as e:
        msg = str(e)
        if "не найден" in msg:
            raise HTTPException(status_code=404, detail=msg)
        raise HTTPException(status_code=400, detail=msg)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception("Ошибка при анализе документа")
        msg = str(e).strip()
        if "OPENROUTER_API_KEY" in msg or "ключ" in msg.lower():
            raise HTTPException(status_code=503, detail="Сервис анализа недоступен: не задан OPENROUTER_API_KEY в .env")
        # Показываем пользователю причину (обрезаем длинные сообщения)
        if len(msg) > 300:
            msg = msg[:297] + "..."
        raise HTTPException(status_code=502, detail=msg or "Ошибка при анализе документа. Попробуйте позже.")


@app.get("/api/documents/{document_id}/results", response_model=list[ResultListItem])
def list_document_results(document_id: int, db: Session = Depends(get_db)):
    """Список результатов анализа по документу (id, document_id, analysis_type, content, created_at)."""
    from backend.models import Document, Result

    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Документ не найден")
    results = db.query(Result).filter(Result.document_id == document_id).order_by(Result.created_at.desc()).all()
    return [
        ResultListItem(
            id=r.id,
            document_id=r.document_id,
            analysis_type=r.analysis_type,
            content=r.content,
            created_at=r.created_at,
        )
        for r in results
    ]


@app.get("/api/results/{result_id}", response_model=ResultDetailResponse)
def get_result(result_id: int, db: Session = Depends(get_db)):
    """Полный результат анализа по id (для страницы результата)."""
    from backend.models import Result

    result = db.query(Result).filter(Result.id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Результат не найден")
    return ResultDetailResponse(
        id=result.id,
        document_id=result.document_id,
        analysis_type=result.analysis_type,
        content=result.content,
        created_at=result.created_at,
    )


@app.get("/api/demo/document")
def demo_document():
    """
    Отдаёт демо-документ (PDF) для просмотра в браузере.
    Нужен для прозрачности: пользователь может открыть документ и увидеть, что именно анализирует ИИ.
    """
    try:
        content = get_demo_pdf_bytes()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Демо-документ не найден.")
    return Response(
        content=content,
        media_type="application/pdf",
        headers={"Content-Disposition": 'inline; filename="demo_report.pdf"'},
    )


@app.post("/api/demo/run", response_model=DemoRunResponse)
def demo_run(body: DemoRunRequest, db: Session = Depends(get_db)):
    """
    Загружает демо-документ из backend/demo/demo_report.pdf для пользователя,
    сохраняет как обычную загрузку, запускает анализ (summary), возвращает result_id.
    На странице результата доступны анализ и AI Magic как для загруженного файла.
    """
    from backend.models import User

    user = db.query(User).filter(User.id == body.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    try:
        content = get_demo_pdf_bytes()
        doc = save_upload(content, DEMO_FILENAME, body.user_id, db)
        result = run_analysis(doc.id, "summary", db, audience=None)
        return DemoRunResponse(document_id=doc.id, result_id=result.id)
    except FileNotFoundError as e:
        logger.warning("Демо-файл не найден: %s", e)
        raise HTTPException(
            status_code=404,
            detail="Демо-файл не найден. Добавьте backend/demo/demo_report.pdf",
        )
    except Exception as e:
        logger.exception("Ошибка демо-режима")
        raise HTTPException(status_code=500, detail="Не удалось запустить демо.")


@app.post("/api/ai-magic", response_model=AIMagicResponse)
def ai_magic(body: AIMagicRequest, db: Session = Depends(get_db)):
    """
    Генерирует AI Magic отчёт: документ + готовые анализы → один запрос к LLM.
    Промпт загружается из docs/AI_MAGIC_PROMPT.md.
    """
    try:
        report = run_ai_magic(body.document_id, db, audience=body.audience)
        return AIMagicResponse(report=report)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        msg = str(e)
        if "не найден" in msg:
            raise HTTPException(status_code=404, detail=msg)
        raise HTTPException(status_code=400, detail=msg)
    except Exception as e:
        logger.exception("Ошибка AI Magic")
        msg = str(e).strip()
        if "OPENROUTER_API_KEY" in msg or "ключ" in msg.lower():
            raise HTTPException(
                status_code=503,
                detail="Сервис недоступен: не задан OPENROUTER_API_KEY в .env",
            )
        if len(msg) > 300:
            msg = msg[:297] + "..."
        raise HTTPException(status_code=502, detail=msg or "Ошибка при генерации отчёта.")


@app.post("/api/export-report")
def export_report(body: ExportReportRequest):
    """
    Генерирует PDF из текста AI Magic отчёта и возвращает файл для скачивания.
    """
    try:
        text = (body.report_text or "").strip()
        if not text:
            text = " "
        pdf_bytes = report_text_to_pdf(text)
    except Exception as e:
        logger.exception("Ошибка генерации PDF отчёта: %s", e)
        raise HTTPException(status_code=500, detail="Не удалось сформировать PDF.")
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="DocMind_Report.pdf"'},
    )


@app.get("/debug/db")
def debug_db():
    """
    Временный эндпоинт: создаёт тестового пользователя (или возвращает существующего) и проверяет БД.
    Удалить или отключить в продакшене.
    """
    db = SessionLocal()
    try:
        from backend.models import User

        user = db.query(User).filter(User.username == "test_user_debug").first()
        if not user:
            user = User(username="test_user_debug")
            db.add(user)
            db.commit()
            db.refresh(user)
            message = "Тестовый пользователь создан"
        else:
            message = "Тестовый пользователь уже существует"
        return {
            "status": "ok",
            "message": message,
            "user_id": user.id,
            "username": user.username,
        }
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()


# Раздача фронтенда: каталог frontend/ в корне проекта
_FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
if not _FRONTEND_DIR.exists():
    _FRONTEND_DIR = Path.cwd() / "frontend"


@app.get("/")
def index():
    """Главная страница — index.html."""
    index_path = _FRONTEND_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Frontend not found. Run from project root.")
    return FileResponse(str(index_path))


if _FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(_FRONTEND_DIR), html=True), name="frontend")
