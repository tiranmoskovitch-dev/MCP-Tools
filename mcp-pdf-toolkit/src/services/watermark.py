"""Watermark service — create and overlay text watermarks on PDFs."""

import io
import math
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas


def _hex_to_rgb(hex_color: str) -> tuple[float, float, float]:
    """Convert hex color string to RGB floats (0-1)."""
    hex_color = hex_color.lstrip("#")
    if len(hex_color) != 6:
        raise ValueError(f"Invalid hex color: #{hex_color}")
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    return r, g, b


def _create_watermark_page(
    text: str,
    position: str,
    opacity: float,
    font_size: int,
    color: str,
    page_width: float,
    page_height: float,
) -> bytes:
    """Create a single-page PDF containing the watermark text."""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(page_width, page_height))

    r, g, b = _hex_to_rgb(color)

    c.saveState()
    c.setFillColorRGB(r, g, b, alpha=opacity)
    c.setFont("Helvetica", font_size)

    text_width = c.stringWidth(text, "Helvetica", font_size)

    if position == "center":
        x = (page_width - text_width) / 2
        y = page_height / 2
        c.drawString(x, y, text)

    elif position == "diagonal":
        c.translate(page_width / 2, page_height / 2)
        angle = math.degrees(math.atan2(page_height, page_width))
        c.rotate(angle)
        c.drawCentredString(0, 0, text)

    elif position == "header":
        x = (page_width - text_width) / 2
        y = page_height - font_size - 20
        c.drawString(x, y, text)

    elif position == "footer":
        x = (page_width - text_width) / 2
        y = 20
        c.drawString(x, y, text)

    else:
        # Default to diagonal for unknown positions
        c.translate(page_width / 2, page_height / 2)
        angle = math.degrees(math.atan2(page_height, page_width))
        c.rotate(angle)
        c.drawCentredString(0, 0, text)

    c.restoreState()
    c.save()
    buf.seek(0)
    return buf.read()


async def add_watermark(
    pdf_path: str,
    output_path: str,
    text: str,
    position: str = "diagonal",
    opacity: float = 0.3,
    font_size: int = 40,
    color: str = "#808080",
) -> dict:
    src = Path(pdf_path)
    if not src.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    if not text or not text.strip():
        raise ValueError("Watermark text cannot be empty.")

    opacity = max(0.0, min(1.0, opacity))
    if position not in ("center", "diagonal", "header", "footer"):
        raise ValueError(
            f"Invalid position '{position}'. Use: center, diagonal, header, footer."
        )

    try:
        reader = PdfReader(str(src))
    except Exception as exc:
        raise RuntimeError(f"Failed to read PDF: {exc}") from exc

    if reader.is_encrypted:
        try:
            reader.decrypt("")
        except Exception:
            raise RuntimeError("PDF is encrypted and cannot be decrypted without a password.")

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    writer = PdfWriter()
    pages_watermarked = 0

    for page in reader.pages:
        box = page.mediabox
        pw = float(box.width)
        ph = float(box.height)

        wm_bytes = _create_watermark_page(text, position, opacity, font_size, color, pw, ph)
        wm_reader = PdfReader(io.BytesIO(wm_bytes))
        wm_page = wm_reader.pages[0]

        page.merge_page(wm_page)
        writer.add_page(page)
        pages_watermarked += 1

    with open(out, "wb") as fh:
        writer.write(fh)

    return {
        "source": str(src.resolve()),
        "output_path": str(out.resolve()),
        "watermark_text": text,
        "position": position,
        "opacity": opacity,
        "pages_watermarked": pages_watermarked,
    }
