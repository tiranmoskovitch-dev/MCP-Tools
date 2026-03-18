from __future__ import annotations

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def add_watermark(
    image_path: str,
    output_path: str | None = None,
    text: str | None = None,
    watermark_image_path: str | None = None,
    position: str = "bottom-right",
    opacity: float = 0.5,
    font_size: int | None = None,
) -> dict:
    if text is None and watermark_image_path is None:
        raise ValueError("Either 'text' or 'watermark_image_path' must be provided")

    valid_positions = {"center", "bottom-right", "bottom-left", "top-right", "top-left", "tile"}
    if position not in valid_positions:
        raise ValueError(f"Invalid position '{position}'. Use: {', '.join(sorted(valid_positions))}")

    opacity = max(0.0, min(1.0, opacity))

    img = Image.open(image_path).convert("RGBA")

    if text:
        result = _apply_text_watermark(img, text, position, opacity, font_size)
        watermark_type = "text"
    else:
        result = _apply_image_watermark(img, watermark_image_path, position, opacity)
        watermark_type = "image"

    out = output_path or image_path
    _save_result(result, out, image_path)

    return {
        "output_path": str(Path(out).resolve()),
        "watermark_type": watermark_type,
        "position": position,
    }


def _apply_text_watermark(
    img: Image.Image,
    text: str,
    position: str,
    opacity: float,
    font_size: int | None,
) -> Image.Image:
    if font_size is None:
        font_size = max(16, min(img.width, img.height) // 20)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except (OSError, IOError):
        try:
            font = ImageFont.truetype("DejaVuSans.ttf", font_size)
        except (OSError, IOError):
            font = ImageFont.load_default()

    # Create text overlay
    txt_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(txt_layer)

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    alpha = round(255 * opacity)
    fill = (255, 255, 255, alpha)

    if position == "tile":
        _tile_text(draw, img.size, text, font, fill, text_width, text_height)
    else:
        x, y = _calc_position(img.size, text_width, text_height, position)
        # Draw shadow for readability
        draw.text((x + 2, y + 2), text, font=font, fill=(0, 0, 0, alpha // 2))
        draw.text((x, y), text, font=font, fill=fill)

    return Image.alpha_composite(img, txt_layer)


def _apply_image_watermark(
    img: Image.Image,
    watermark_path: str,
    position: str,
    opacity: float,
) -> Image.Image:
    wm = Image.open(watermark_path).convert("RGBA")

    # Scale watermark if larger than 1/4 of base image
    max_wm_w = img.width // 4
    max_wm_h = img.height // 4
    if wm.width > max_wm_w or wm.height > max_wm_h:
        ratio = min(max_wm_w / wm.width, max_wm_h / wm.height)
        wm = wm.resize((round(wm.width * ratio), round(wm.height * ratio)), Image.LANCZOS)

    # Apply opacity
    if opacity < 1.0:
        alpha = wm.split()[3]
        alpha = alpha.point(lambda p: round(p * opacity))
        wm.putalpha(alpha)

    if position == "tile":
        return _tile_image(img, wm)

    x, y = _calc_position(img.size, wm.width, wm.height, position)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    layer.paste(wm, (x, y))
    return Image.alpha_composite(img, layer)


def _calc_position(
    img_size: tuple[int, int],
    wm_w: int,
    wm_h: int,
    position: str,
) -> tuple[int, int]:
    iw, ih = img_size
    margin = max(10, min(iw, ih) // 50)

    positions = {
        "center": ((iw - wm_w) // 2, (ih - wm_h) // 2),
        "top-left": (margin, margin),
        "top-right": (iw - wm_w - margin, margin),
        "bottom-left": (margin, ih - wm_h - margin),
        "bottom-right": (iw - wm_w - margin, ih - wm_h - margin),
    }
    return positions.get(position, positions["bottom-right"])


def _tile_text(
    draw: ImageDraw.ImageDraw,
    img_size: tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple,
    text_width: int,
    text_height: int,
) -> None:
    spacing_x = text_width + max(40, text_width // 2)
    spacing_y = text_height + max(40, text_height // 2)

    y = 0
    while y < img_size[1]:
        x = 0
        while x < img_size[0]:
            draw.text((x, y), text, font=font, fill=fill)
            x += spacing_x
        y += spacing_y


def _tile_image(base: Image.Image, wm: Image.Image) -> Image.Image:
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    spacing_x = wm.width + max(20, wm.width // 4)
    spacing_y = wm.height + max(20, wm.height // 4)

    y = 0
    while y < base.height:
        x = 0
        while x < base.width:
            layer.paste(wm, (x, y))
            x += spacing_x
        y += spacing_y

    return Image.alpha_composite(base, layer)


def _save_result(img: Image.Image, path: str, original_path: str) -> None:
    ext = Path(path).suffix.lower()
    fmt_map = {
        ".jpg": "JPEG", ".jpeg": "JPEG", ".png": "PNG",
        ".webp": "WEBP", ".tiff": "TIFF", ".tif": "TIFF",
        ".bmp": "BMP", ".gif": "GIF",
    }
    fmt = fmt_map.get(ext, "PNG")

    if fmt == "JPEG":
        img = img.convert("RGB")
        img.save(path, format=fmt, quality=95)
    else:
        img.save(path, format=fmt)
