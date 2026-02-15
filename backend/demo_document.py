"""
Демо-документ для быстрого показа возможностей (кнопка «Use demo document»).
Генерирует одностраничный PDF с текстом.
"""

from io import BytesIO


def get_demo_pdf_bytes() -> bytes:
    """Возвращает байты PDF демо-документа и имя файла."""
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    pdf.set_auto_page_break(auto=True, margin=15)
    text = (
        "DocMind Demo Document\n\n"
        "This is a sample document for demonstration. "
        "It contains key points about project planning and risk management.\n\n"
        "Key topics:\n"
        "- Define clear objectives and milestones.\n"
        "- Identify risks early and plan mitigation.\n"
        "- Communicate with stakeholders regularly.\n"
        "- Review progress and adjust the plan as needed.\n\n"
        "Conclusion: Good planning and risk awareness help deliver projects successfully."
    )
    for line in text.split("\n"):
        pdf.multi_cell(0, 6, line)
    buf = BytesIO()
    pdf.output(buf)
    buf.seek(0)
    return buf.getvalue()


DEMO_FILENAME = "demo_document.pdf"
