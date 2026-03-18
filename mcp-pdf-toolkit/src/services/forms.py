"""PDF form filling service — list and fill form fields using pypdf."""

from pathlib import Path

from pypdf import PdfReader, PdfWriter


def _get_field_info(field: dict) -> dict:
    """Extract readable info from a PDF form field dictionary."""
    field_type_map = {
        "/Tx": "text",
        "/Btn": "button/checkbox",
        "/Ch": "choice/dropdown",
        "/Sig": "signature",
    }
    raw_type = str(field.get("/FT", "unknown"))
    return {
        "name": field.get("/T", "unnamed"),
        "type": field_type_map.get(raw_type, raw_type),
        "value": field.get("/V", None),
        "default": field.get("/DV", None),
    }


async def fill_form(
    pdf_path: str,
    output_path: str,
    fields: dict | None = None,
) -> dict:
    src = Path(pdf_path)
    if not src.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    try:
        reader = PdfReader(str(src))
    except Exception as exc:
        raise RuntimeError(f"Failed to read PDF: {exc}") from exc

    if reader.is_encrypted:
        try:
            reader.decrypt("")
        except Exception:
            raise RuntimeError("PDF is encrypted and cannot be decrypted without a password.")

    # Discover available form fields
    available_fields: list[dict] = []
    if reader.get_fields():
        for name, field in reader.get_fields().items():
            info = _get_field_info(field)
            info["name"] = name  # override with the dict key which is more reliable
            available_fields.append(info)

    # If no fields to fill, return listing mode
    if not fields:
        return {
            "mode": "list",
            "source": str(src.resolve()),
            "total_fields": len(available_fields),
            "available_fields": available_fields,
            "note": "No fields dict provided. Pass 'fields' with {field_name: value} to fill the form.",
        }

    # Validate requested fields exist
    known_names = {f["name"] for f in available_fields}
    unknown = set(fields.keys()) - known_names
    if unknown and available_fields:
        # Warn but don't fail — some PDFs have fields not returned by get_fields()
        pass

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    writer = PdfWriter()
    writer.append(reader)

    filled_count = 0
    for page_num in range(len(writer.pages)):
        try:
            writer.update_page_form_field_values(writer.pages[page_num], fields)
            filled_count += 1
        except Exception:
            continue

    # Flatten if possible to preserve filled values in non-form readers
    try:
        for page in writer.pages:
            if "/Annots" in page:
                for annot in page["/Annots"]:
                    annot_obj = annot.get_object()
                    if annot_obj.get("/Subtype") == "/Widget":
                        annot_obj.update({"/Ff": 1})  # read-only flag
    except Exception:
        pass

    with open(out, "wb") as fh:
        writer.write(fh)

    return {
        "mode": "fill",
        "source": str(src.resolve()),
        "output_path": str(out.resolve()),
        "fields_requested": len(fields),
        "pages_processed": filled_count,
        "available_fields": available_fields,
    }
