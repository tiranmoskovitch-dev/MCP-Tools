"""MCP Server: QR Code Factory
Generate and decode QR codes, vCards, WiFi configs, styled QR codes.
"""
import asyncio
import json
import traceback

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from src.services.generator import QRGeneratorService
from src.services.decoder import QRDecoderService

server = Server("mcp-qrcode")


TOOLS = [
    Tool(
        name="generate_qr",
        description="Generate a QR code from arbitrary data. Returns base64-encoded PNG/SVG or saves to a file path.",
        inputSchema={
            "type": "object",
            "properties": {
                "data": {
                    "type": "string",
                    "description": "The data to encode in the QR code",
                },
                "format": {
                    "type": "string",
                    "enum": ["png", "svg"],
                    "default": "png",
                    "description": "Output image format (png or svg)",
                },
                "size": {
                    "type": "integer",
                    "default": 10,
                    "description": "Box size in pixels for each QR module",
                },
                "border": {
                    "type": "integer",
                    "default": 4,
                    "description": "Border size in modules around the QR code",
                },
                "error_correction": {
                    "type": "string",
                    "enum": ["L", "M", "Q", "H"],
                    "default": "M",
                    "description": "Error correction level: L(7%), M(15%), Q(25%), H(30%)",
                },
                "output_path": {
                    "type": "string",
                    "description": "File path to save the QR code. If omitted, returns base64-encoded image.",
                },
            },
            "required": ["data"],
        },
    ),
    Tool(
        name="decode_qr",
        description="Decode one or more QR codes from an image. Provide either a file path or base64-encoded image.",
        inputSchema={
            "type": "object",
            "properties": {
                "image_path": {
                    "type": "string",
                    "description": "Path to the image file containing QR code(s)",
                },
                "image_base64": {
                    "type": "string",
                    "description": "Base64-encoded image data containing QR code(s)",
                },
            },
            "required": [],
        },
    ),
    Tool(
        name="generate_vcard_qr",
        description="Generate a QR code containing a vCard 3.0 contact card. Scan with a phone to add a contact.",
        inputSchema={
            "type": "object",
            "properties": {
                "first_name": {
                    "type": "string",
                    "description": "Contact first name",
                },
                "last_name": {
                    "type": "string",
                    "description": "Contact last name",
                },
                "email": {
                    "type": "string",
                    "description": "Email address",
                },
                "phone": {
                    "type": "string",
                    "description": "Phone number",
                },
                "organization": {
                    "type": "string",
                    "description": "Organization/company name",
                },
                "title": {
                    "type": "string",
                    "description": "Job title",
                },
                "url": {
                    "type": "string",
                    "description": "Website URL",
                },
                "address": {
                    "type": "string",
                    "description": "Physical address",
                },
                "output_path": {
                    "type": "string",
                    "description": "File path to save the QR code. If omitted, returns base64.",
                },
            },
            "required": ["first_name", "last_name"],
        },
    ),
    Tool(
        name="generate_wifi_qr",
        description="Generate a QR code for WiFi network configuration. Scan with a phone to auto-connect.",
        inputSchema={
            "type": "object",
            "properties": {
                "ssid": {
                    "type": "string",
                    "description": "WiFi network name (SSID)",
                },
                "password": {
                    "type": "string",
                    "description": "WiFi password",
                },
                "security": {
                    "type": "string",
                    "enum": ["WPA", "WEP", "nopass"],
                    "default": "WPA",
                    "description": "Security type",
                },
                "hidden": {
                    "type": "boolean",
                    "default": False,
                    "description": "Whether the network is hidden",
                },
                "output_path": {
                    "type": "string",
                    "description": "File path to save the QR code. If omitted, returns base64.",
                },
            },
            "required": ["ssid", "password"],
        },
    ),
    Tool(
        name="styled_qr",
        description="Generate a styled QR code with custom colors and optional logo embedded in the center.",
        inputSchema={
            "type": "object",
            "properties": {
                "data": {
                    "type": "string",
                    "description": "The data to encode in the QR code",
                },
                "fill_color": {
                    "type": "string",
                    "default": "#000000",
                    "description": "QR module color (hex, e.g. '#000000')",
                },
                "back_color": {
                    "type": "string",
                    "default": "#FFFFFF",
                    "description": "Background color (hex, e.g. '#FFFFFF')",
                },
                "logo_path": {
                    "type": "string",
                    "description": "Path to a logo image to embed in the QR center",
                },
                "logo_size_percent": {
                    "type": "integer",
                    "default": 20,
                    "description": "Logo size as a percentage of QR code size (1-40)",
                },
                "output_path": {
                    "type": "string",
                    "description": "File path to save the QR code. If omitted, returns base64.",
                },
            },
            "required": ["data"],
        },
    ),
    Tool(
        name="bulk_generate",
        description="Generate multiple QR codes at once and save them to a directory.",
        inputSchema={
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "data": {
                                "type": "string",
                                "description": "Data to encode",
                            },
                            "filename": {
                                "type": "string",
                                "description": "Output filename (auto-generated from data hash if omitted)",
                            },
                        },
                        "required": ["data"],
                    },
                    "description": "List of items to generate QR codes for",
                },
                "format": {
                    "type": "string",
                    "enum": ["png", "svg"],
                    "default": "png",
                    "description": "Output image format",
                },
                "output_dir": {
                    "type": "string",
                    "description": "Directory to save generated QR code files",
                },
            },
            "required": ["items", "output_dir"],
        },
    ),
]


@server.list_tools()
async def list_tools() -> list[Tool]:
    return TOOLS


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        result = _dispatch(name, arguments)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        error_response = {
            "error": str(e),
            "tool": name,
            "traceback": traceback.format_exc(),
        }
        return [TextContent(type="text", text=json.dumps(error_response, indent=2))]


def _dispatch(name: str, arguments: dict) -> dict:
    if name == "generate_qr":
        return QRGeneratorService.generate_qr(
            data=arguments["data"],
            fmt=arguments.get("format", "png"),
            size=arguments.get("size", 10),
            border=arguments.get("border", 4),
            error_correction=arguments.get("error_correction", "M"),
            output_path=arguments.get("output_path"),
        )

    elif name == "decode_qr":
        return QRDecoderService.decode_qr(
            image_path=arguments.get("image_path"),
            image_base64=arguments.get("image_base64"),
        )

    elif name == "generate_vcard_qr":
        return QRGeneratorService.generate_vcard_qr(
            first_name=arguments["first_name"],
            last_name=arguments["last_name"],
            email=arguments.get("email"),
            phone=arguments.get("phone"),
            organization=arguments.get("organization"),
            title=arguments.get("title"),
            url=arguments.get("url"),
            address=arguments.get("address"),
            output_path=arguments.get("output_path"),
        )

    elif name == "generate_wifi_qr":
        return QRGeneratorService.generate_wifi_qr(
            ssid=arguments["ssid"],
            password=arguments["password"],
            security=arguments.get("security", "WPA"),
            hidden=arguments.get("hidden", False),
            output_path=arguments.get("output_path"),
        )

    elif name == "styled_qr":
        return QRGeneratorService.generate_styled_qr(
            data=arguments["data"],
            fill_color=arguments.get("fill_color", "#000000"),
            back_color=arguments.get("back_color", "#FFFFFF"),
            logo_path=arguments.get("logo_path"),
            logo_size_percent=arguments.get("logo_size_percent", 20),
            output_path=arguments.get("output_path"),
        )

    elif name == "bulk_generate":
        return QRGeneratorService.bulk_generate(
            items=arguments["items"],
            fmt=arguments.get("format", "png"),
            output_dir=arguments["output_dir"],
        )

    else:
        return {"error": f"Unknown tool: {name}"}


async def run():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
