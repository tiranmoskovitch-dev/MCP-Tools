import base64
import io
import os
from typing import Any, Optional

from PIL import Image

try:
    from pyzbar.pyzbar import decode as pyzbar_decode
    from pyzbar.pyzbar import ZBarSymbol
    PYZBAR_AVAILABLE = True
except ImportError:
    PYZBAR_AVAILABLE = False


class QRDecoderService:

    @staticmethod
    def decode_qr(
        image_path: Optional[str] = None,
        image_base64: Optional[str] = None,
    ) -> dict[str, Any]:
        if not PYZBAR_AVAILABLE:
            return {
                "error": "pyzbar is not available. Install pyzbar and the zbar system library. "
                         "On Windows: pip install pyzbar (zbar DLLs bundled). "
                         "On Linux: sudo apt-get install libzbar0. "
                         "On macOS: brew install zbar.",
                "decoded": [],
                "count": 0,
            }

        if not image_path and not image_base64:
            return {
                "error": "Either image_path or image_base64 must be provided",
                "decoded": [],
                "count": 0,
            }

        try:
            if image_path:
                if not os.path.isfile(image_path):
                    return {
                        "error": f"File not found: {image_path}",
                        "decoded": [],
                        "count": 0,
                    }
                img = Image.open(image_path)
            else:
                image_bytes = base64.b64decode(image_base64)
                img = Image.open(io.BytesIO(image_bytes))

            img = img.convert("RGB")
            decoded_objects = pyzbar_decode(img)

            results = []
            for obj in decoded_objects:
                rect = obj.rect
                results.append({
                    "data": obj.data.decode("utf-8", errors="replace"),
                    "type": obj.type,
                    "rect": {
                        "left": rect.left,
                        "top": rect.top,
                        "width": rect.width,
                        "height": rect.height,
                    },
                    "quality": obj.quality if hasattr(obj, "quality") else None,
                })

            return {
                "decoded": results,
                "count": len(results),
            }

        except Exception as e:
            return {
                "error": f"Failed to decode image: {str(e)}",
                "decoded": [],
                "count": 0,
            }
