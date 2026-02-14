"""
DocMind — минимальный FastAPI backend.
Фаза 1: health-check. Фаза 2: инициализация БД.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.database import Base, SessionLocal, engine
from backend import models  # регистрация моделей у Base
from backend.file_upload import ensure_uploads_dir


@asynccontextmanager
async def lifespan(app: FastAPI):
    """При старте приложения создаём таблицы в БД и каталог для загрузок."""
    Base.metadata.create_all(bind=engine)
    ensure_uploads_dir()
    yield
    # при завершении ничего не делаем


app = FastAPI(title="DocMind", version="0.1.0", lifespan=lifespan)


@app.get("/health")
def health():
    """Проверка доступности сервера."""
    return {"status": "ok"}


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
