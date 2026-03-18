import base64
import hashlib
import io
import os
from pathlib import Path
from typing import Any, Optional

import qrcode
import qrcode.image.svg
from PIL import Image


ERROR_CORRECTION_MAP = {
    "L": qrcode.constants.ERROR_CORRECT_L,
    "M": qrcode.constants.ERROR_CORRECT_M,
    "Q": qrcode.constants.ERROR_CORRECT_Q,
    "H": qrcode.constants.ERROR_CORRECT_H,
}


class QRGeneratorService:

    @staticmethod
    def generate_qr(
        data: str,
        fmt: str = "png",
        size: int = 10,
        border: int = 4,
        error_correction: str = "M",
        output_path: Optional[str] = None,
        fill_color: str = "#000000",
        back_color: str = "#FFFFFF",
    ) -> dict[str, Any]:
        ec = ERROR_CORRECTION_MAP.get(error_correction.upper(), qrcode.constants.ERROR_CORRECT_M)

        qr = qrcode.QRCode(
            version=None,
            error_correction=ec,
            box_size=size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)

        if fmt.lower() == "svg":
            img = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage)
            buffer = io.BytesIO()
            img.save(buffer)
            svg_string = buffer.getvalue().decode("utf-8")

            if output_path:
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(svg_string)
                return {
                    "file_path": os.path.abspath(output_path),
                    "format": "svg",
                    "data_length": len(data),
                    "version": qr.version,
                }

            return {
                "svg": svg_string,
                "format": "svg",
                "data_length": len(data),
                "version": qr.version,
            }

        # PNG format
        img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGBA")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(buffer.getvalue())
            return {
                "file_path": os.path.abspath(output_path),
                "format": "png",
                "data_length": len(data),
                "version": qr.version,
            }

        encoded = base64.b64encode(buffer.getvalue()).decode()
        return {
            "image_base64": encoded,
            "format": "png",
            "data_length": len(data),
            "version": qr.version,
        }

    @staticmethod
    def generate_vcard_qr(
        first_name: str,
        last_name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        organization: Optional[str] = None,
        title: Optional[str] = None,
        url: Optional[str] = None,
        address: Optional[str] = None,
        output_path: Optional[str] = None,
    ) -> dict[str, Any]:
        lines = [
            "BEGIN:VCARD",
            "VERSION:3.0",
            f"N:{last_name};{first_name};;;",
            f"FN:{first_name} {last_name}",
        ]
        if email:
            lines.append(f"EMAIL:{email}")
        if phone:
            lines.append(f"TEL:{phone}")
        if organization:
            lines.append(f"ORG:{organization}")
        if title:
            lines.append(f"TITLE:{title}")
        if url:
            lines.append(f"URL:{url}")
        if address:
            lines.append(f"ADR:{address}")
        lines.append("END:VCARD")

        vcard_text = "\r\n".join(lines)

        result = QRGeneratorService.generate_qr(
            data=vcard_text,
            fmt="png",
            size=10,
            border=4,
            error_correction="M",
            output_path=output_path,
        )
        result["vcard_text"] = vcard_text
        return result

    @staticmethod
    def generate_wifi_qr(
        ssid: str,
        password: str,
        security: str = "WPA",
        hidden: bool = False,
        output_path: Optional[str] = None,
    ) -> dict[str, Any]:
        hidden_str = "true" if hidden else "false"
        wifi_string = f"WIFI:T:{security};S:{ssid};P:{password};H:{hidden_str};;"

        result = QRGeneratorService.generate_qr(
            data=wifi_string,
            fmt="png",
            size=10,
            border=4,
            error_correction="M",
            output_path=output_path,
        )
        result["wifi_string"] = wifi_string
        return result

    @staticmethod
    def generate_styled_qr(
        data: str,
        fill_color: str = "#000000",
        back_color: str = "#FFFFFF",
        logo_path: Optional[str] = None,
        logo_size_percent: int = 20,
        output_path: Optional[str] = None,
    ) -> dict[str, Any]:
        ec = qrcode.constants.ERROR_CORRECT_H if logo_path else qrcode.constants.ERROR_CORRECT_M

        qr = qrcode.QRCode(
            version=None,
            error_correction=ec,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGBA")

        if logo_path:
            if not os.path.isfile(logo_path):
                raise FileNotFoundError(f"Logo file not found: {logo_path}")

            logo = Image.open(logo_path).convert("RGBA")
            qr_width, qr_height = img.size
            logo_max = int(min(qr_width, qr_height) * logo_size_percent / 100)
            logo.thumbnail((logo_max, logo_max), Image.LANCZOS)

            logo_w, logo_h = logo.size
            pos_x = (qr_width - logo_w) // 2
            pos_y = (qr_height - logo_h) // 2

            white_bg = Image.new("RGBA", (logo_w, logo_h), back_color)
            white_bg.paste(logo, (0, 0), logo)
            img.paste(white_bg, (pos_x, pos_y), white_bg)

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(buffer.getvalue())
            return {
                "file_path": os.path.abspath(output_path),
                "format": "png",
                "data_length": len(data),
                "version": qr.version,
                "fill_color": fill_color,
                "back_color": back_color,
                "has_logo": logo_path is not None,
            }

        encoded = base64.b64encode(buffer.getvalue()).decode()
        return {
            "image_base64": encoded,
            "format": "png",
            "data_length": len(data),
            "version": qr.version,
            "fill_color": fill_color,
            "back_color": back_color,
            "has_logo": logo_path is not None,
        }

    @staticmethod
    def bulk_generate(
        items: list[dict[str, Any]],
        fmt: str = "png",
        output_dir: str = ".",
    ) -> dict[str, Any]:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        results = []

        for item in items:
            data = item.get("data", "")
            filename = item.get("filename")

            if not data:
                results.append({
                    "data": data,
                    "status": "error",
                    "error": "Empty data field",
                })
                continue

            if not filename:
                data_hash = hashlib.sha256(data.encode()).hexdigest()[:12]
                ext = "svg" if fmt.lower() == "svg" else "png"
                filename = f"qr_{data_hash}.{ext}"

            file_path = os.path.join(output_dir, filename)

            try:
                result = QRGeneratorService.generate_qr(
                    data=data,
                    fmt=fmt,
                    output_path=file_path,
                )
                results.append({
                    "data": data,
                    "file_path": result.get("file_path", file_path),
                    "status": "success",
                    "version": result.get("version"),
                })
            except Exception as e:
                results.append({
                    "data": data,
                    "status": "error",
                    "error": str(e),
                })

        successful = sum(1 for r in results if r["status"] == "success")
        failed = sum(1 for r in results if r["status"] == "error")

        return {
            "total": len(items),
            "successful": successful,
            "failed": failed,
            "output_dir": os.path.abspath(output_dir),
            "results": results,
        }
