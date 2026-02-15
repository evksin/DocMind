"""
Демо-документ для кнопки «Попробовать на примере».
Загружает готовый PDF из backend/demo/demo_report.pdf и обрабатывает его как загруженный пользователем файл.
"""

from pathlib import Path

from backend.database import BASE_DIR

# Путь к демо-PDF относительно backend/
DEMO_PDF_PATH = BASE_DIR / "demo" / "demo_report.pdf"
DEMO_FILENAME = "demo_report.pdf"


def get_demo_pdf_bytes() -> bytes:
    """
    Читает байты демо-документа из backend/demo/demo_report.pdf.
    Обрабатывается далее как обычная загрузка: save_upload → run_analysis → AI Magic на странице результата.
    """
    if not DEMO_PDF_PATH.exists():
        raise FileNotFoundError(f"Демо-файл не найден: {DEMO_PDF_PATH}")
    return DEMO_PDF_PATH.read_bytes()
