from __future__ import annotations

import os
from pathlib import Path

from PIL import Image

FORMAT_MAP = {
    "png": "PNG",
    "jpeg": "JPEG",
    "jpg": "JPEG",
    "webp": "WEBP",
    "tiff": "TIFF",
    "bmp": "BMP",
    "gif": "GIF",
    "ico": "ICO",
}

LOSSY_FORMATS = {"JPEG", "WEBP"}


def convert_format(
    image_path: str,
    output_format: str,
    output_path: str | None = None,
    quality: int = 85,
) -> dict:
    output_format_lower = output_format.lower()
    pil_format = FORMAT_MAP.get(output_format_lower)
    if pil_format is None:
        raise ValueError(f"Unsupported format '{output_format}'. Use: {', '.join(FORMAT_MAP)}")

    quality = max(1, min(100, quality))

    img = Image.open(image_path)
    input_format = img.format or "UNKNOWN"

    # Handle animated GIFs
    if hasattr(img, "n_frames") and img.n_frames > 1:
        img.seek(0)

    # Build output path
    if output_path is None:
        p = Path(image_path)
        ext = output_format_lower if output_format_lower != "jpeg" else "jpg"
        output_path = str(p.with_suffix(f".{ext}"))

    # RGBA -> RGB for JPEG
    if pil_format == "JPEG" and img.mode in ("RGBA", "P", "LA"):
        bg = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "P":
            img = img.convert("RGBA")
        bg.paste(img, mask=img.split()[-1] if "A" in img.mode else None)
        img = bg
    elif pil_format == "JPEG" and img.mode not in ("RGB", "L"):
        img = img.convert("RGB")

    # Handle 16-bit images
    if img.mode == "I;16":
        img = img.convert("I").point(lambda x: x >> 8).convert("L")

    save_kwargs: dict = {}
    if pil_format in LOSSY_FORMATS:
        save_kwargs["quality"] = quality
    if pil_format == "PNG":
        save_kwargs["optimize"] = True
    if pil_format == "ICO":
        # ICO needs specific sizes
        save_kwargs["sizes"] = [(min(img.width, 256), min(img.height, 256))]

    # Preserve ICC profile
    icc = img.info.get("icc_profile")
    if icc and pil_format in ("JPEG", "PNG", "TIFF", "WEBP"):
        save_kwargs["icc_profile"] = icc

    img.save(output_path, format=pil_format, **save_kwargs)

    return {
        "output_path": str(Path(output_path).resolve()),
        "input_format": input_format,
        "output_format": pil_format,
        "file_size_bytes": os.path.getsize(output_path),
    }
