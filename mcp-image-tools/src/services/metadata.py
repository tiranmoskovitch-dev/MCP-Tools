from __future__ import annotations

import os
from pathlib import Path

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


def strip_metadata(
    image_path: str,
    output_path: str | None = None,
    keep_icc: bool = True,
) -> dict:
    original_size_bytes = os.path.getsize(image_path)
    img = Image.open(image_path)

    # Detect what metadata exists
    metadata_removed = []

    if img.info.get("exif"):
        metadata_removed.append("EXIF")
    if img.info.get("icc_profile"):
        if not keep_icc:
            metadata_removed.append("ICC_PROFILE")
    if img.info.get("xmp"):
        metadata_removed.append("XMP")
    # Check for IPTC via tag
    if hasattr(img, "tag_v2"):
        iptc_tag = 33723  # IPTC-NAA
        if iptc_tag in (img.tag_v2 or {}):
            metadata_removed.append("IPTC")
    # Photoshop data
    if img.info.get("photoshop"):
        metadata_removed.append("Photoshop")
    # PNG text chunks
    for key in ("Comment", "Description", "Author", "Software", "Creation Time"):
        if key in img.info:
            if "PNG_TEXT" not in metadata_removed:
                metadata_removed.append("PNG_TEXT")

    if not metadata_removed and not keep_icc:
        metadata_removed.append("NONE")

    # Create clean image from pixel data only
    fmt = img.format or _format_from_path(image_path)

    # Handle animated GIFs
    if hasattr(img, "n_frames") and img.n_frames > 1:
        img.seek(0)

    clean = img.copy()

    # Remove all info
    clean.info = {}

    out = output_path or image_path
    save_kwargs: dict = {}

    if fmt == "JPEG":
        if clean.mode in ("RGBA", "P", "LA"):
            clean = clean.convert("RGB")
        elif clean.mode not in ("RGB", "L"):
            clean = clean.convert("RGB")
        save_kwargs["quality"] = 95
    elif fmt == "PNG":
        save_kwargs["optimize"] = True

    # Optionally preserve ICC profile
    if keep_icc:
        icc = img.info.get("icc_profile") if hasattr(img, "info") else None
        # Re-read from original since we cleared info
        original = Image.open(image_path)
        icc = original.info.get("icc_profile")
        if icc:
            save_kwargs["icc_profile"] = icc
            if "ICC_PROFILE" in metadata_removed:
                metadata_removed.remove("ICC_PROFILE")

    clean.save(out, format=fmt, **save_kwargs)
    new_size_bytes = os.path.getsize(out)

    return {
        "output_path": str(Path(out).resolve()),
        "metadata_removed": metadata_removed if metadata_removed else ["NONE"],
        "original_size_bytes": original_size_bytes,
        "new_size_bytes": new_size_bytes,
    }


def read_exif(
    image_path: str,
    include_thumbnail: bool = False,
) -> dict:
    img = Image.open(image_path)

    result: dict = {
        "file": str(Path(image_path).resolve()),
        "format": img.format,
        "mode": img.mode,
        "dimensions": list(img.size),
    }

    # Try to get EXIF data
    exif_data = None
    try:
        exif_data = img._getexif()
    except (AttributeError, Exception):
        pass

    if exif_data is None:
        result["exif"] = None
        result["message"] = "No EXIF data found"
        return result

    parsed: dict = {}
    gps_info: dict = {}

    for tag_id, value in exif_data.items():
        tag_name = TAGS.get(tag_id, f"Unknown_{tag_id}")

        # Skip thumbnail data unless requested
        if tag_name == "JPEGThumbnail" and not include_thumbnail:
            continue
        if tag_name == "MakerNote":
            parsed["MakerNote"] = "<binary data>"
            continue

        if tag_name == "GPSInfo":
            gps_info = _parse_gps(value)
            continue

        # Convert IFDRational and other special types to serializable values
        parsed[tag_name] = _make_serializable(value)

    # Build structured output
    exif_result: dict = {}

    # Camera info
    if "Make" in parsed:
        exif_result["camera_make"] = parsed["Make"]
    if "Model" in parsed:
        exif_result["camera_model"] = parsed["Model"]

    # Date/time
    if "DateTimeOriginal" in parsed:
        exif_result["date_time_original"] = parsed["DateTimeOriginal"]
    elif "DateTime" in parsed:
        exif_result["date_time"] = parsed["DateTime"]
    if "DateTimeDigitized" in parsed:
        exif_result["date_time_digitized"] = parsed["DateTimeDigitized"]

    # Exposure settings
    if "ExposureTime" in parsed:
        exif_result["exposure_time"] = parsed["ExposureTime"]
    if "FNumber" in parsed:
        exif_result["f_stop"] = parsed["FNumber"]
    if "ISOSpeedRatings" in parsed:
        exif_result["iso"] = parsed["ISOSpeedRatings"]
    if "FocalLength" in parsed:
        exif_result["focal_length"] = parsed["FocalLength"]
    if "FocalLengthIn35mmFilm" in parsed:
        exif_result["focal_length_35mm"] = parsed["FocalLengthIn35mmFilm"]

    # Image info
    if "ImageWidth" in parsed:
        exif_result["image_width"] = parsed["ImageWidth"]
    if "ImageLength" in parsed:
        exif_result["image_height"] = parsed["ImageLength"]
    if "ExifImageWidth" in parsed:
        exif_result["exif_image_width"] = parsed["ExifImageWidth"]
    if "ExifImageHeight" in parsed:
        exif_result["exif_image_height"] = parsed["ExifImageHeight"]
    if "Orientation" in parsed:
        exif_result["orientation"] = _orientation_label(parsed["Orientation"])
    if "Software" in parsed:
        exif_result["software"] = parsed["Software"]

    # Flash and metering
    if "Flash" in parsed:
        exif_result["flash"] = _flash_label(parsed["Flash"])
    if "WhiteBalance" in parsed:
        exif_result["white_balance"] = "Auto" if parsed["WhiteBalance"] == 0 else "Manual"
    if "MeteringMode" in parsed:
        exif_result["metering_mode"] = _metering_label(parsed["MeteringMode"])
    if "ExposureProgram" in parsed:
        exif_result["exposure_program"] = _exposure_program_label(parsed["ExposureProgram"])
    if "ExposureBiasValue" in parsed:
        exif_result["exposure_bias"] = parsed["ExposureBiasValue"]

    # GPS
    if gps_info:
        exif_result["gps"] = gps_info

    # Lens info
    if "LensModel" in parsed:
        exif_result["lens_model"] = parsed["LensModel"]
    if "LensMake" in parsed:
        exif_result["lens_make"] = parsed["LensMake"]

    result["exif"] = exif_result

    # Include all raw tags if the structured extraction missed anything important
    result["all_tags"] = parsed

    return result


def _parse_gps(gps_ifd: dict) -> dict:
    gps_data: dict = {}

    # Parse GPS tag names
    parsed_tags: dict = {}
    for tag_id, value in gps_ifd.items():
        tag_name = GPSTAGS.get(tag_id, f"Unknown_{tag_id}")
        parsed_tags[tag_name] = value

    try:
        if "GPSLatitude" in parsed_tags and "GPSLatitudeRef" in parsed_tags:
            lat = _dms_to_decimal(parsed_tags["GPSLatitude"])
            if parsed_tags["GPSLatitudeRef"] == "S":
                lat = -lat
            gps_data["latitude"] = round(lat, 6)

        if "GPSLongitude" in parsed_tags and "GPSLongitudeRef" in parsed_tags:
            lon = _dms_to_decimal(parsed_tags["GPSLongitude"])
            if parsed_tags["GPSLongitudeRef"] == "W":
                lon = -lon
            gps_data["longitude"] = round(lon, 6)

        if "GPSAltitude" in parsed_tags:
            alt = float(parsed_tags["GPSAltitude"])
            ref = parsed_tags.get("GPSAltitudeRef", 0)
            if ref == 1:
                alt = -alt
            gps_data["altitude_meters"] = round(alt, 2)

        if "GPSDateStamp" in parsed_tags:
            gps_data["date_stamp"] = str(parsed_tags["GPSDateStamp"])

        if "GPSTimeStamp" in parsed_tags:
            ts = parsed_tags["GPSTimeStamp"]
            try:
                gps_data["time_stamp"] = f"{int(float(ts[0]))}:{int(float(ts[1]))}:{float(ts[2]):.2f}"
            except (IndexError, TypeError, ValueError):
                gps_data["time_stamp"] = str(ts)

    except (TypeError, ValueError, ZeroDivisionError):
        gps_data["parse_error"] = "Could not parse GPS coordinates"

    return gps_data


def _dms_to_decimal(dms) -> float:
    """Convert DMS (degrees, minutes, seconds) to decimal degrees.

    Handles both IFDRational tuples like ((degrees, 1), (minutes, 1), (seconds, 100))
    and direct float/Fraction values.
    """
    parts = []
    for val in dms:
        if isinstance(val, tuple) and len(val) == 2:
            # (numerator, denominator) rational
            parts.append(val[0] / val[1] if val[1] != 0 else 0.0)
        else:
            parts.append(float(val))

    degrees = parts[0]
    minutes = parts[1] if len(parts) > 1 else 0
    seconds = parts[2] if len(parts) > 2 else 0

    return degrees + minutes / 60 + seconds / 3600


def _make_serializable(value):
    """Convert PIL EXIF values to JSON-serializable types."""
    if isinstance(value, bytes):
        try:
            return value.decode("utf-8", errors="replace")
        except Exception:
            return f"<binary {len(value)} bytes>"
    if isinstance(value, tuple):
        if len(value) == 2 and all(isinstance(v, (int, float)) for v in value):
            # IFDRational (num, denom)
            if value[1] != 0:
                result = value[0] / value[1]
                return result if result != int(result) else int(result)
            return 0
        return [_make_serializable(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _make_serializable(v) for k, v in value.items()}
    if isinstance(value, (int, float, str, bool)):
        return value
    # Handle IFDRational objects from Pillow
    try:
        return float(value)
    except (TypeError, ValueError):
        return str(value)


def _orientation_label(val) -> str:
    labels = {
        1: "Normal",
        2: "Mirrored horizontal",
        3: "Rotated 180",
        4: "Mirrored vertical",
        5: "Mirrored horizontal, rotated 270 CW",
        6: "Rotated 90 CW",
        7: "Mirrored horizontal, rotated 90 CW",
        8: "Rotated 270 CW",
    }
    return labels.get(val, f"Unknown ({val})")


def _flash_label(val) -> str:
    fired = bool(val & 0x01)
    return "Fired" if fired else "Did not fire"


def _metering_label(val) -> str:
    labels = {
        0: "Unknown", 1: "Average", 2: "Center-weighted average",
        3: "Spot", 4: "Multi-spot", 5: "Pattern", 6: "Partial",
    }
    return labels.get(val, f"Unknown ({val})")


def _exposure_program_label(val) -> str:
    labels = {
        0: "Not defined", 1: "Manual", 2: "Normal program",
        3: "Aperture priority", 4: "Shutter priority",
        5: "Creative program", 6: "Action program",
        7: "Portrait mode", 8: "Landscape mode",
    }
    return labels.get(val, f"Unknown ({val})")


def _format_from_path(path: str) -> str:
    ext = Path(path).suffix.lower()
    fmt_map = {
        ".jpg": "JPEG", ".jpeg": "JPEG", ".png": "PNG",
        ".webp": "WEBP", ".tiff": "TIFF", ".tif": "TIFF",
        ".bmp": "BMP", ".gif": "GIF",
    }
    return fmt_map.get(ext, "PNG")
