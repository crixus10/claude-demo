"""
pdf_reader.py
Extracts text and renders the first page as a base64 image from a PDF file.
"""

import base64
import pdfplumber
import fitz  # PyMuPDF


def extract_text(pdf_path: str) -> str:
    """Return all text content from the PDF."""
    text_parts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n".join(text_parts)


def render_first_page_as_base64(pdf_path: str, dpi: int = 150) -> str:
    """Render the first page of the PDF as a base64-encoded PNG."""
    doc = fitz.open(pdf_path)
    page = doc[0]
    zoom = dpi / 72
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    png_bytes = pix.tobytes("png")
    doc.close()
    return base64.standard_b64encode(png_bytes).decode("utf-8")
