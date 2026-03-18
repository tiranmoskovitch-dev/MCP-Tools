"""PDF to images converter — extracts pages as images using pdf2image or embedded image fallback."""

from pathlib import Path

from pypdf import PdfReader


async def pdf_to_images(
    pdf_path: str,
    output_dir: str,
    format: str = "png",
    dpi: int = 150,
    pages: list[int] | None = None,
) -> dict:
    src = Path(pdf_path)
    if not src.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    if format not in ("png", "jpeg"):
        raise ValueError(f"Unsupported format '{format}'. Use 'png' or 'jpeg'.")

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

    total_pages = len(reader.pages)
    if pages:
        for p in pages:
            if p < 1 or p > total_pages:
                raise ValueError(f"Page {p} out of range (1-{total_pages}).")
        target_pages = pages
    else:
        target_pages = list(range(1, total_pages + 1))

    stem = src.stem
    ext = "jpg" if format == "jpeg" else "png"
    output_files: list[str] = []
    method = "unknown"

    # Strategy 1: pdf2image (requires poppler)
    try:
        from pdf2image import convert_from_path

        images = convert_from_path(
            str(src),
            dpi=dpi,
            fmt=format,
            first_page=min(target_pages),
            last_page=max(target_pages),
        )

        # pdf2image returns images for the range min..max, map back to requested pages
        base_page = min(target_pages)
        for page_num in target_pages:
            img_idx = page_num - base_page
            if img_idx < len(images):
                out_file = out_dir / f"{stem}_page{page_num}.{ext}"
                pil_format = "JPEG" if format == "jpeg" else "PNG"
                images[img_idx].save(str(out_file), pil_format)
                output_files.append(str(out_file.resolve()))

        method = "pdf2image"

    except (ImportError, Exception):
        # Strategy 2: Extract embedded images from each page using pypdf
        from PIL import Image
        import io

        method = "embedded_extraction"

        for page_num in target_pages:
            page = reader.pages[page_num - 1]
            images_on_page = []

            if "/XObject" in page.get("/Resources", {}):
                x_objects = page["/Resources"]["/XObject"].get_object()
                for obj_name in x_objects:
                    obj = x_objects[obj_name].get_object()
                    if obj.get("/Subtype") == "/Image":
                        try:
                            width = int(obj["/Width"])
                            height = int(obj["/Height"])
                            color_space = obj.get("/ColorSpace", "/DeviceRGB")
                            if isinstance(color_space, list):
                                color_space = str(color_space[0])
                            else:
                                color_space = str(color_space)

                            data = obj.get_data()

                            # Determine PIL mode from color space
                            if "Gray" in color_space:
                                mode = "L"
                            elif "CMYK" in color_space:
                                mode = "CMYK"
                            else:
                                mode = "RGB"

                            # Check for common filters
                            filters = obj.get("/Filter", "")
                            if isinstance(filters, list):
                                filters = [str(f) for f in filters]
                            else:
                                filters = [str(filters)]

                            if "/DCTDecode" in filters:
                                # JPEG data
                                img = Image.open(io.BytesIO(data))
                            elif "/FlateDecode" in filters or "/Filter" not in obj:
                                expected_size = width * height * (len(mode))
                                if len(data) >= expected_size:
                                    img = Image.frombytes(mode, (width, height), data)
                                else:
                                    continue
                            elif "/JPXDecode" in filters:
                                img = Image.open(io.BytesIO(data))
                            else:
                                continue

                            images_on_page.append(img)
                        except Exception:
                            continue

            if images_on_page:
                # If multiple images on a page, save the largest one
                images_on_page.sort(key=lambda i: i.size[0] * i.size[1], reverse=True)
                img = images_on_page[0]
                if img.mode == "CMYK":
                    img = img.convert("RGB")
                out_file = out_dir / f"{stem}_page{page_num}.{ext}"
                pil_format = "JPEG" if format == "jpeg" else "PNG"
                img.save(str(out_file), pil_format)
                output_files.append(str(out_file.resolve()))

    return {
        "source": str(src.resolve()),
        "method": method,
        "format": format,
        "dpi": dpi,
        "pages_requested": len(target_pages),
        "images_created": len(output_files),
        "output_files": output_files,
        "note": (
            "Used embedded image extraction (fallback). For full page rendering, "
            "install: pip install pdf2image (and Poppler binaries)."
            if method == "embedded_extraction"
            else "Pages rendered via pdf2image with Poppler."
        ),
    }
