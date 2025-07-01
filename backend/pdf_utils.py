# pdf_utils.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

def convert_text_to_pdf(text):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    x_margin = 40
    y_margin = 750
    line_height = 14

    lines = text.split('\n')
    for line in lines:
        if y_margin < 50:
            c.showPage()
            y_margin = 750
        c.drawString(x_margin, y_margin, line)
        y_margin -= line_height

    c.save()
    buffer.seek(0)
    return buffer

