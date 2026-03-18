from __future__ import annotations

import os
import time
import glob as globmod
from pathlib import Path

from src.services.resize import resize_image
from src.services.convert import convert_format
from src.services.compress import compress_image
from src.services.watermark import add_watermark
from src.services.metadata import strip_metadata

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".tiff", ".tif"}


def batch_process(
    input_dir: str,
    output_dir: str,
    operations: list[dict],
    pattern: str = "*.{jpg,jpeg,png,webp,gif,bmp,tiff}",
) -> dict:
    if not os.path.isdir(input_dir):
        raise ValueError(f"Input directory does not exist: {input_dir}")

    os.makedirs(output_dir, exist_ok=True)

    # Collect matching files
    files = _find_images(input_dir, pattern)

    if not files:
        return {
            "processed": [],
            "total_processed": 0,
            "total_failed": 0,
            "total_time_ms": 0,
        }

    start = time.perf_counter()
    results = []
    total_failed = 0

    for file_path in sorted(files):
        file_result = _process_single(file_path, input_dir, output_dir, operations)
        results.append(file_result)
        if file_result["status"] == "failed":
            total_failed += 1

    elapsed_ms = round((time.perf_counter() - start) * 1000)

    return {
        "processed": results,
        "total_processed": len(results) - total_failed,
        "total_failed": total_failed,
        "total_time_ms": elapsed_ms,
    }


def _process_single(
    file_path: str,
    input_dir: str,
    output_dir: str,
    operations: list[dict],
) -> dict:
    rel_path = os.path.relpath(file_path, input_dir)
    output_file = os.path.join(output_dir, rel_path)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    try:
        # Copy original to output first so operations can work in-place
        from PIL import Image
        img = Image.open(file_path)
        _save_copy(img, output_file)

        current_path = output_file

        for op in operations:
            action = op.get("action", "").lower()
            current_path = _apply_operation(current_path, action, op)

        return {
            "file": rel_path,
            "output_path": str(Path(current_path).resolve()),
            "status": "success",
        }

    except Exception as e:
        return {
            "file": rel_path,
            "status": "failed",
            "error": str(e),
        }


def _apply_operation(current_path: str, action: str, params: dict) -> str:
    if action == "resize":
        result = resize_image(
            image_path=current_path,
            output_path=current_path,
            width=params.get("width"),
            height=params.get("height"),
            maintain_aspect=params.get("maintain_aspect", True),
            resample=params.get("resample", "lanczos"),
        )
        return result["output_path"]

    elif action == "convert":
        fmt = params.get("format", "png")
        p = Path(current_path)
        ext_map = {
            "jpeg": ".jpg", "jpg": ".jpg", "png": ".png",
            "webp": ".webp", "tiff": ".tiff", "bmp": ".bmp",
            "gif": ".gif", "ico": ".ico",
        }
        new_ext = ext_map.get(fmt.lower(), f".{fmt.lower()}")
        new_path = str(p.with_suffix(new_ext))
        result = convert_format(
            image_path=current_path,
            output_format=fmt,
            output_path=new_path,
            quality=params.get("quality", 85),
        )
        # Remove old file if extension changed
        if current_path != result["output_path"] and os.path.exists(current_path):
            try:
                os.remove(current_path)
            except OSError:
                pass
        return result["output_path"]

    elif action == "compress":
        result = compress_image(
            image_path=current_path,
            output_path=current_path,
            quality=params.get("quality", 75),
            max_width=params.get("max_width"),
            max_height=params.get("max_height"),
        )
        return result["output_path"]

    elif action == "strip_metadata":
        result = strip_metadata(
            image_path=current_path,
            output_path=current_path,
            keep_icc=params.get("keep_icc", True),
        )
        return result["output_path"]

    elif action == "watermark":
        result = add_watermark(
            image_path=current_path,
            output_path=current_path,
            text=params.get("text"),
            watermark_image_path=params.get("watermark_image_path"),
            position=params.get("position", "bottom-right"),
            opacity=params.get("opacity", 0.5),
            font_size=params.get("font_size"),
        )
        return result["output_path"]

    else:
        raise ValueError(f"Unknown batch action: '{action}'")


def _find_images(input_dir: str, pattern: str) -> list[str]:
    # Handle brace expansion patterns like *.{jpg,jpeg,png}
    if "{" in pattern and "}" in pattern:
        # Extract the brace part
        prefix = pattern[:pattern.index("{")]
        brace_content = pattern[pattern.index("{") + 1:pattern.index("}")]
        suffix = pattern[pattern.index("}") + 1:]
        extensions = [ext.strip() for ext in brace_content.split(",")]
        patterns = [f"{prefix}{ext}{suffix}" for ext in extensions]
    else:
        patterns = [pattern]

    files: list[str] = []
    for pat in patterns:
        full_pattern = os.path.join(input_dir, "**", pat)
        found = globmod.glob(full_pattern, recursive=True)
        files.extend(found)

    # Also try non-recursive
    for pat in patterns:
        full_pattern = os.path.join(input_dir, pat)
        found = globmod.glob(full_pattern)
        files.extend(found)

    # Deduplicate and filter to actual image files
    seen = set()
    unique: list[str] = []
    for f in files:
        real = os.path.realpath(f)
        if real not in seen and os.path.isfile(f):
            ext = Path(f).suffix.lower()
            if ext in IMAGE_EXTENSIONS:
                seen.add(real)
                unique.append(f)

    return unique


def _save_copy(img, path: str) -> None:
    from PIL import Image as PILImage
    ext = Path(path).suffix.lower()
    fmt_map = {
        ".jpg": "JPEG", ".jpeg": "JPEG", ".png": "PNG",
        ".webp": "WEBP", ".tiff": "TIFF", ".tif": "TIFF",
        ".bmp": "BMP", ".gif": "GIF",
    }
    fmt = fmt_map.get(ext, "PNG")

    save_kwargs: dict = {}
    if fmt == "JPEG":
        if img.mode in ("RGBA", "P", "LA"):
            bg = PILImage.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            if "A" in img.mode:
                bg.paste(img, mask=img.split()[-1])
            else:
                bg.paste(img)
            img = bg
        elif img.mode not in ("RGB", "L"):
            img = img.convert("RGB")
        save_kwargs["quality"] = 95
    elif fmt == "PNG":
        save_kwargs["optimize"] = True

    icc = img.info.get("icc_profile")
    if icc and fmt in ("JPEG", "PNG", "TIFF", "WEBP"):
        save_kwargs["icc_profile"] = icc

    img.save(path, format=fmt, **save_kwargs)
