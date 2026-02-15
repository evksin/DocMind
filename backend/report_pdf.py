"""
Генерация PDF из текста AI Magic отчёта для экспорта.
Поддерживает кириллицу через Unicode-шрифт (Arial/DejaVu или системный).
"""

import os
from io import BytesIO
from pathlib import Path


def _find_unicode_font() -> str | None:
    """Возвращает путь к TTF-шрифту с поддержкой кириллицы или None."""
    root = Path(__file__).resolve().parent.parent
    backend_dir = Path(__file__).resolve().parent
    candidates = [
        backend_dir / "fonts" / "dejavu-sans-ttf-2.37" / "ttf" / "DejaVuSans.ttf",
        backend_dir / "fonts" / "DejaVuSans.ttf",
        root / "fonts" / "DejaVuSans.ttf",
        root / "font" / "DejaVuSans.ttf",
    ]
    windir = os.environ.get("WINDIR", "")
    if windir:
        candidates.extend([
            Path(windir) / "Fonts" / "arial.ttf",
            Path(windir) / "Fonts" / "Arial.ttf",
        ])
    for path in candidates:
        if path.exists():
            return str(path)
    return None


def _sanitize_ascii(text: str) -> str:
    """Оставляет только ASCII (0–127), остальное заменяет на '?'. Гарантированно работает с Helvetica на любом сервере."""
    return "".join(c if ord(c) < 128 else "?" for c in text)


def _safe_line(s: str) -> str:
    """Убирает управляющие и непечатаемые символы (только ASCII)."""
    return "".join(c for c in s if 32 <= ord(c) <= 126 or c in "\n\t")


def _strip_control_chars(s: str) -> str:
    """Убирает только управляющие символы (0–31, 127), сохраняет кириллицу."""
    return "".join(c for c in s if ord(c) >= 32 and ord(c) != 127 or c in "\n\t")


def report_text_to_pdf(report_text: str) -> bytes:
    """Строит PDF из текста отчёта (plain text, переносы сохраняются). На сервере без шрифтов использует только ASCII."""
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(20, 20, 20)

    use_unicode = False
    font_path = _find_unicode_font()
    if font_path:
        try:
            pdf.add_font("UnicodeFont", "", font_path)
            pdf.set_font("UnicodeFont", size=11)
            use_unicode = True
        except Exception:
            pdf.set_font("Helvetica", size=11)
    else:
        pdf.set_font("Helvetica", size=11)

    # Явная ширина ячейки, чтобы избежать "Not enough horizontal space" (epw = usable width)
    cell_w = getattr(pdf, "epw", None) or (pdf.w - pdf.l_margin - pdf.r_margin)
    if cell_w <= 0:
        cell_w = 170  # A4: 210 - 20*2 mm

    def write_line(s: str) -> None:
        t = (s or "").strip()
        if not t:
            pdf.ln(4)
            return
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(cell_w, 6, t)

    text = (report_text or "").strip()
    if not text:
        write_line("No content.")
    else:
        for raw_line in text.replace("\r", "").split("\n"):
            line = raw_line.strip()
            if not line:
                pdf.ln(4)
                continue
            if use_unicode:
                line = _strip_control_chars(line)
            else:
                line = _sanitize_ascii(_safe_line(line))
            if not line:
                pdf.ln(4)
                continue
            try:
                write_line(line)
            except Exception:
                fallback = _sanitize_ascii(_safe_line(raw_line))[:200].strip() or " "
                write_line(fallback)
    buf = BytesIO()
    pdf.output(buf)
    buf.seek(0)
    return buf.getvalue()
