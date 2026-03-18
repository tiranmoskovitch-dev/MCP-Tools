from __future__ import annotations

import os
from pathlib import Path

from PIL import Image

RESAMPLE_METHODS = {
    "lanczos": Image.LANCZOS,
    "bilinear": Image.BILINEAR,
    "bicubic": Image.BICUBIC,
    "nearest": Image.NEAREST,
}


def resize_image(
    image_path: str,
    output_path: str | None = None,
    width: int | None = None,
    height: int | None = None,
    maintain_aspect: bool = True,
    resample: str = "lanczos",
) -> dict:
    if width is None and height is None:
        raise ValueError("At least one of width or height must be provided")

    resample_filter = RESAMPLE_METHODS.get(resample.lower())
    if resample_filter is None:
        raise ValueError(f"Invalid resample method '{resample}'. Use: {', '.join(RESAMPLE_METHODS)}")

    img = Image.open(image_path)
    # Handle animated GIFs — work on first frame
    if hasattr(img, "n_frames") and img.n_frames > 1:
        img.seek(0)

    original_size = img.size

    if maintain_aspect:
        if width and height:
            # Fit within the box while maintaining aspect ratio
            ratio = min(width / img.width, height / img.height)
            new_width = round(img.width * ratio)
            new_height = round(img.height * ratio)
        elif width:
            ratio = width / img.width
            new_width = width
            new_height = round(img.height * ratio)
        else:
            ratio = height / img.height
            new_width = round(img.width * ratio)
            new_height = height
    else:
        new_width = width or img.width
        new_height = height or img.height

    resized = img.resize((new_width, new_height), resample_filter)

    out = output_path or image_path
    _save_image(resized, out, img)

    return {
        "output_path": str(Path(out).resolve()),
        "original_size": list(original_size),
        "new_size": [new_width, new_height],
        "file_size_bytes": os.path.getsize(out),
    }


def _save_image(img: Image.Image, path: str, original: Image.Image) -> None:
    save_kwargs: dict = {}
    fmt = _format_from_path(path)

    if fmt == "JPEG" and img.mode in ("RGBA", "P", "LA"):
        img = img.convert("RGB")
    if fmt == "JPEG":
        save_kwargs["quality"] = 95
    if fmt == "PNG":
        save_kwargs["optimize"] = True

    # Preserve ICC profile if present
    icc = original.info.get("icc_profile")
    if icc:
        save_kwargs["icc_profile"] = icc

    img.save(path, format=fmt, **save_kwargs)


def _format_from_path(path: str) -> str:
    ext = Path(path).suffix.lower()
    fmt_map = {
        ".jpg": "JPEG", ".jpeg": "JPEG",
        ".png": "PNG", ".webp": "WEBP",
        ".tiff": "TIFF", ".tif": "TIFF",
        ".bmp": "BMP", ".gif": "GIF",
        ".ico": "ICO",
    }
    return fmt_map.get(ext, "PNG")
