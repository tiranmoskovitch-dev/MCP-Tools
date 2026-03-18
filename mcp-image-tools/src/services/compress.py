from __future__ import annotations

import os
from pathlib import Path

from PIL import Image

FORMAT_EXT_MAP = {
    "JPEG": ".jpg", "PNG": ".png", "WEBP": ".webp",
    "TIFF": ".tiff", "BMP": ".bmp", "GIF": ".gif",
}

EXT_FORMAT_MAP = {
    ".jpg": "JPEG", ".jpeg": "JPEG", ".png": "PNG",
    ".webp": "WEBP", ".tiff": "TIFF", ".tif": "TIFF",
    ".bmp": "BMP", ".gif": "GIF",
}


def compress_image(
    image_path: str,
    output_path: str | None = None,
    quality: int = 75,
    max_width: int | None = None,
    max_height: int | None = None,
    format: str | None = None,
) -> dict:
    quality = max(1, min(100, quality))
    original_size_bytes = os.path.getsize(image_path)

    img = Image.open(image_path)
    input_format = img.format or "PNG"

    # Handle animated GIFs
    if hasattr(img, "n_frames") and img.n_frames > 1:
        img.seek(0)

    # Determine output format
    if format:
        out_format = format.upper()
        if out_format == "JPG":
            out_format = "JPEG"
    else:
        out_format = input_format

    # Downscale if needed
    resized = False
    if max_width and img.width > max_width:
        ratio = max_width / img.width
        img = img.resize((max_width, round(img.height * ratio)), Image.LANCZOS)
        resized = True
    if max_height and img.height > max_height:
        ratio = max_height / img.height
        img = img.resize((round(img.width * ratio), max_height), Image.LANCZOS)
        resized = True

    # Build output path
    if output_path is None:
        p = Path(image_path)
        if format:
            ext = FORMAT_EXT_MAP.get(out_format, p.suffix)
            output_path = str(p.with_suffix(ext))
        else:
            output_path = image_path

    # Mode conversions
    if out_format == "JPEG" and img.mode in ("RGBA", "P", "LA"):
        bg = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "P":
            img = img.convert("RGBA")
        if "A" in img.mode:
            bg.paste(img, mask=img.split()[-1])
        else:
            bg.paste(img)
        img = bg
    elif out_format == "JPEG" and img.mode not in ("RGB", "L"):
        img = img.convert("RGB")

    # Handle 16-bit
    if img.mode == "I;16":
        img = img.convert("I").point(lambda x: x >> 8).convert("L")

    save_kwargs: dict = {}

    if out_format == "JPEG":
        save_kwargs["quality"] = quality
        save_kwargs["optimize"] = True
    elif out_format == "PNG":
        save_kwargs["optimize"] = True
        # Map quality 1-100 to compress_level 9-0 (higher quality = lower compression)
        save_kwargs["compress_level"] = max(0, min(9, round(9 * (1 - quality / 100))))
    elif out_format == "WEBP":
        save_kwargs["quality"] = quality
        save_kwargs["method"] = 6  # Best compression
    elif out_format == "TIFF":
        save_kwargs["compression"] = "tiff_deflate"

    # Preserve ICC profile
    icc = img.info.get("icc_profile")
    if icc and out_format in ("JPEG", "PNG", "TIFF", "WEBP"):
        save_kwargs["icc_profile"] = icc

    img.save(output_path, format=out_format, **save_kwargs)
    compressed_size_bytes = os.path.getsize(output_path)

    ratio = original_size_bytes / compressed_size_bytes if compressed_size_bytes > 0 else 0

    return {
        "output_path": str(Path(output_path).resolve()),
        "original_size_bytes": original_size_bytes,
        "compressed_size_bytes": compressed_size_bytes,
        "compression_ratio": round(ratio, 2),
        "dimensions": list(img.size),
    }
