"""Text extraction and OCR service — uses pdfplumber for high-quality text extraction."""

from pathlib import Path

import pdfplumber


async def extract_text(
    pdf_path: str,
    pages: list[int] | None = None,
    format: str = "plain",
) -> dict:
    src = Path(pdf_path)
    if not src.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    try:
        pdf = pdfplumber.open(str(src))
    except Exception as exc:
        raise RuntimeError(f"Failed to open PDF: {exc}") from exc

    total_pages = len(pdf.pages)

    if pages:
        for p in pages:
            if p < 1 or p > total_pages:
                raise ValueError(f"Page {p} out of range (1-{total_pages}).")
        target_indices = [p - 1 for p in pages]
    else:
        target_indices = list(range(total_pages))

    results: list[dict] = []
    total_chars = 0

    for idx in target_indices:
        page = pdf.pages[idx]
        page_num = idx + 1

        if format == "structured":
            words = page.extract_words(extra_attrs=["fontname", "size"])
            text = page.extract_text() or ""
            structured_words = []
            for w in words:
                structured_words.append({
                    "text": w.get("text", ""),
                    "x0": round(w.get("x0", 0), 2),
                    "y0": round(w.get("top", 0), 2),
                    "x1": round(w.get("x1", 0), 2),
                    "y1": round(w.get("bottom", 0), 2),
                    "font": w.get("fontname", "unknown"),
                    "size": round(w.get("size", 0), 1),
                })
            tables = page.extract_tables()
            results.append({
                "page": page_num,
                "text": text,
                "chars": len(text),
                "words": structured_words,
                "tables": tables if tables else [],
            })
            total_chars += len(text)
        else:
            text = page.extract_text() or ""
            results.append({
                "page": page_num,
                "text": text,
                "chars": len(text),
            })
            total_chars += len(text)

    pdf.close()

    return {
        "source": str(src.resolve()),
        "format": format,
        "total_pages": total_pages,
        "pages_extracted": len(results),
        "total_chars": total_chars,
        "content": results,
    }


async def pdf_ocr(
    pdf_path: str,
    pages: list[int] | None = None,
    language: str = "eng",
) -> dict:
    src = Path(pdf_path)
    if not src.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    try:
        pdf = pdfplumber.open(str(src))
    except Exception as exc:
        raise RuntimeError(f"Failed to open PDF: {exc}") from exc

    total_pages = len(pdf.pages)

    if pages:
        for p in pages:
            if p < 1 or p > total_pages:
                raise ValueError(f"Page {p} out of range (1-{total_pages}).")
        target_indices = [p - 1 for p in pages]
    else:
        target_indices = list(range(total_pages))

    results: list[dict] = []
    total_chars = 0
    extraction_method = "pdfplumber"
    low_text_pages: list[int] = []

    for idx in target_indices:
        page = pdf.pages[idx]
        page_num = idx + 1
        text = page.extract_text() or ""
        char_count = len(text.strip())
        total_chars += char_count

        if char_count < 50:
            low_text_pages.append(page_num)

        results.append({
            "page": page_num,
            "text": text,
            "chars": char_count,
        })

    pdf.close()

    # Try pytesseract if pdfplumber yielded very little text
    tesseract_available = False
    if low_text_pages and total_chars < 100:
        try:
            import pytesseract  # noqa: F401
            tesseract_available = True
            extraction_method = "pytesseract"

            # Re-extract with Tesseract via pdf2image
            try:
                from pdf2image import convert_from_path

                images = convert_from_path(str(src), dpi=300)
                results = []
                total_chars = 0
                for idx in target_indices:
                    if idx < len(images):
                        page_num = idx + 1
                        text = pytesseract.image_to_string(images[idx], lang=language)
                        char_count = len(text.strip())
                        total_chars += char_count
                        results.append({
                            "page": page_num,
                            "text": text,
                            "chars": char_count,
                        })
            except ImportError:
                extraction_method = "pdfplumber"
                tesseract_available = False
        except ImportError:
            pass

    confidence_note = "Text extracted via pdfplumber (embedded text layer)."
    if low_text_pages and not tesseract_available:
        confidence_note = (
            f"Pages with very little text detected: {low_text_pages}. "
            "This may be a scanned/image-based PDF. For true OCR, install: "
            "pip install pytesseract pdf2image (and Tesseract binary + Poppler)."
        )
    elif extraction_method == "pytesseract":
        confidence_note = f"OCR performed via Tesseract (language: {language})."

    return {
        "source": str(src.resolve()),
        "extraction_method": extraction_method,
        "total_pages": total_pages,
        "pages_extracted": len(results),
        "total_chars": total_chars,
        "confidence_note": confidence_note,
        "content": results,
    }
