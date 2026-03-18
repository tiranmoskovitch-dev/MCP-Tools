"""PDF split service — split a PDF by pages, ranges, or every-N chunks."""

from pathlib import Path

from pypdf import PdfReader, PdfWriter


def _parse_ranges(range_str: str, max_page: int) -> list[tuple[int, int]]:
    """Parse range strings like '1-3,5-7' into (start, end) tuples (1-indexed, inclusive)."""
    segments: list[tuple[int, int]] = []
    for part in range_str.split(","):
        part = part.strip()
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            start, end = int(start_s.strip()), int(end_s.strip())
        else:
            start = end = int(part)
        if start < 1 or end > max_page or start > end:
            raise ValueError(
                f"Invalid range '{part}': must be within 1-{max_page} and start <= end."
            )
        segments.append((start, end))
    return segments


def _write_pages(reader: PdfReader, page_indices: list[int], output_file: Path) -> int:
    """Write selected 0-indexed pages to a new PDF. Returns page count."""
    writer = PdfWriter()
    for idx in page_indices:
        writer.add_page(reader.pages[idx])
    with open(output_file, "wb") as fh:
        writer.write(fh)
    return len(page_indices)


async def split_pdf(
    pdf_path: str,
    output_dir: str,
    mode: str = "pages",
    pages: list[int] | None = None,
    ranges: list[str] | None = None,
    every_n: int | None = None,
) -> dict:
    src = Path(pdf_path)
    if not src.exists():
        raise FileNotFoundError(f"Source PDF not found: {pdf_path}")

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        reader = PdfReader(str(src))
    except Exception as exc:
        raise RuntimeError(f"Failed to read PDF: {exc}") from exc

    if reader.is_encrypted:
        try:
            reader.decrypt("")
        except Exception:
            raise RuntimeError("PDF is encrypted and cannot be decrypted without a password.")

    total = len(reader.pages)
    stem = src.stem
    output_files: list[dict] = []

    if mode == "pages":
        if not pages:
            raise ValueError("Mode 'pages' requires a non-empty 'pages' list.")
        for p in pages:
            if p < 1 or p > total:
                raise ValueError(f"Page {p} out of range (1-{total}).")
        for p in pages:
            out_file = out_dir / f"{stem}_page{p}.pdf"
            count = _write_pages(reader, [p - 1], out_file)
            output_files.append({"path": str(out_file.resolve()), "pages": count})

    elif mode == "ranges":
        if not ranges:
            raise ValueError("Mode 'ranges' requires a non-empty 'ranges' list.")
        for idx, range_str in enumerate(ranges):
            segments = _parse_ranges(range_str, total)
            page_indices: list[int] = []
            for start, end in segments:
                page_indices.extend(range(start - 1, end))
            out_file = out_dir / f"{stem}_range{idx + 1}.pdf"
            count = _write_pages(reader, page_indices, out_file)
            output_files.append({"path": str(out_file.resolve()), "pages": count})

    elif mode == "every_n":
        if not every_n or every_n < 1:
            raise ValueError("Mode 'every_n' requires a positive integer 'every_n'.")
        chunk_num = 0
        for start in range(0, total, every_n):
            chunk_num += 1
            end = min(start + every_n, total)
            page_indices = list(range(start, end))
            out_file = out_dir / f"{stem}_chunk{chunk_num}.pdf"
            count = _write_pages(reader, page_indices, out_file)
            output_files.append({"path": str(out_file.resolve()), "pages": count})

    else:
        raise ValueError(f"Unknown split mode: '{mode}'. Use 'pages', 'ranges', or 'every_n'.")

    return {
        "source": str(src.resolve()),
        "mode": mode,
        "total_source_pages": total,
        "output_files": output_files,
        "files_created": len(output_files),
    }
