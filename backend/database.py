"""
Подключение к SQLite и настройка SQLAlchemy для DocMind.
"""

import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Файл БД рядом с backend (backend/docmind.db)
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "docmind.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

# check_same_thread=False нужен для использования сессий в FastAPI
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Генератор сессии БД для FastAPI Depends."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
