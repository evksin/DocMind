"""
Генерация PDF из текста AI Magic отчёта для экспорта.
"""

from io import BytesIO


def report_text_to_pdf(report_text: str) -> bytes:
    """Строит PDF из текста отчёта (plain text, переносы сохраняются)."""
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(20, 20, 20)

    text = (report_text or "").strip()
    if not text:
        pdf.multi_cell(0, 6, "No content.")
    else:
        for line in text.replace("\r", "").split("\n"):
            line = line.strip()
            if not line:
                pdf.ln(4)
                continue
            pdf.multi_cell(0, 6, line)
    buf = BytesIO()
    pdf.output(buf)
    buf.seek(0)
    return buf.getvalue()
