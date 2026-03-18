"""PDF merge service — combines multiple PDFs into a single output file."""

from pathlib import Path

from pypdf import PdfReader, PdfWriter


async def merge_pdfs(pdf_paths: list[str], output_path: str) -> dict:
    if not pdf_paths or len(pdf_paths) < 2:
        raise ValueError("At least two PDF paths are required for merging.")

    resolved_paths: list[Path] = []
    for p in pdf_paths:
        fp = Path(p)
        if not fp.exists():
            raise FileNotFoundError(f"Source PDF not found: {p}")
        if not fp.suffix.lower() == ".pdf":
            raise ValueError(f"Not a PDF file: {p}")
        resolved_paths.append(fp)

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    writer = PdfWriter()
    total_pages = 0

    for fp in resolved_paths:
        try:
            reader = PdfReader(str(fp))
        except Exception as exc:
            raise RuntimeError(f"Failed to read {fp.name}: {exc}") from exc

        if reader.is_encrypted:
            try:
                reader.decrypt("")
            except Exception:
                raise RuntimeError(
                    f"PDF is encrypted and cannot be decrypted without a password: {fp.name}"
                )

        for page in reader.pages:
            writer.add_page(page)
            total_pages += 1

    with open(out, "wb") as fh:
        writer.write(fh)

    return {
        "output_path": str(out.resolve()),
        "total_pages": total_pages,
        "source_files": len(resolved_paths),
    }
