"""MCP Server: PDF Toolkit — production-grade PDF operations.

Seven tools: merge, split, extract text, fill forms, watermark, OCR, PDF-to-images.
Uses the correct MCP pattern: one list_tools handler, one call_tool dispatcher.
"""

import asyncio
import json
import traceback

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from src.services.merger import merge_pdfs
from src.services.splitter import split_pdf
from src.services.extractor import extract_text, pdf_ocr
from src.services.forms import fill_form
from src.services.watermark import add_watermark
from src.services.converter import pdf_to_images

server = Server("mcp-pdf-toolkit")

# ---------------------------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------------------------

TOOLS = [
    Tool(
        name="merge_pdfs",
        description=(
            "Merge multiple PDF files into a single output PDF. "
            "Combines all pages from the source files in the order provided."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "pdf_paths": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of absolute file paths to the PDFs to merge (minimum 2).",
                    "minItems": 2,
                },
                "output_path": {
                    "type": "string",
                    "description": "Absolute file path for the merged output PDF.",
                },
            },
            "required": ["pdf_paths", "output_path"],
        },
    ),
    Tool(
        name="split_pdf",
        description=(
            "Split a PDF into multiple files by specific pages, page ranges, or every N pages. "
            "Three modes: 'pages' extracts individual pages, 'ranges' extracts page ranges "
            "(e.g. '1-3,5-7'), 'every_n' splits into equal chunks."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "pdf_path": {
                    "type": "string",
                    "description": "Absolute path to the source PDF.",
                },
                "output_dir": {
                    "type": "string",
                    "description": "Directory where split PDFs will be saved.",
                },
                "mode": {
                    "type": "string",
                    "enum": ["pages", "ranges", "every_n"],
                    "description": "Split mode: 'pages', 'ranges', or 'every_n'.",
                },
                "pages": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "Page numbers to extract (1-indexed). Required for 'pages' mode.",
                },
                "ranges": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Page ranges like '1-3,5-7'. Required for 'ranges' mode.",
                },
                "every_n": {
                    "type": "integer",
                    "description": "Split into chunks of N pages. Required for 'every_n' mode.",
                    "minimum": 1,
                },
            },
            "required": ["pdf_path", "output_dir", "mode"],
        },
    ),
    Tool(
        name="extract_text",
        description=(
            "Extract text content from a PDF using pdfplumber. Supports plain text or "
            "structured format with bounding boxes, font info, and tables."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "pdf_path": {
                    "type": "string",
                    "description": "Absolute path to the PDF file.",
                },
                "pages": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "Specific page numbers to extract (1-indexed). Default: all pages.",
                },
                "format": {
                    "type": "string",
                    "enum": ["plain", "structured"],
                    "description": "Output format. 'plain' = text only, 'structured' = text + layout info.",
                    "default": "plain",
                },
            },
            "required": ["pdf_path"],
        },
    ),
    Tool(
        name="fill_form",
        description=(
            "List or fill PDF form fields. If 'fields' is omitted, returns all available "
            "form fields with their types and current values (listing mode). If 'fields' is "
            "provided, fills the form and saves to output_path."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "pdf_path": {
                    "type": "string",
                    "description": "Absolute path to the PDF form.",
                },
                "output_path": {
                    "type": "string",
                    "description": "Absolute path for the filled output PDF.",
                },
                "fields": {
                    "type": "object",
                    "description": "Dictionary of {field_name: value} pairs to fill. Omit to list fields.",
                    "additionalProperties": {"type": "string"},
                },
            },
            "required": ["pdf_path", "output_path"],
        },
    ),
    Tool(
        name="add_watermark",
        description=(
            "Add a text watermark to every page of a PDF. Supports center, diagonal, "
            "header, and footer positions with configurable opacity, font size, and color."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "pdf_path": {
                    "type": "string",
                    "description": "Absolute path to the source PDF.",
                },
                "output_path": {
                    "type": "string",
                    "description": "Absolute path for the watermarked output PDF.",
                },
                "text": {
                    "type": "string",
                    "description": "Watermark text to overlay.",
                },
                "position": {
                    "type": "string",
                    "enum": ["center", "diagonal", "header", "footer"],
                    "description": "Watermark position on each page.",
                    "default": "diagonal",
                },
                "opacity": {
                    "type": "number",
                    "description": "Watermark opacity from 0.0 (invisible) to 1.0 (solid).",
                    "default": 0.3,
                    "minimum": 0,
                    "maximum": 1,
                },
                "font_size": {
                    "type": "integer",
                    "description": "Font size for the watermark text.",
                    "default": 40,
                },
                "color": {
                    "type": "string",
                    "description": "Hex color code for the watermark (e.g. '#808080').",
                    "default": "#808080",
                },
            },
            "required": ["pdf_path", "output_path", "text"],
        },
    ),
    Tool(
        name="pdf_ocr",
        description=(
            "Extract text from a PDF, with OCR fallback for scanned documents. "
            "Uses pdfplumber as the primary method. If very little text is found, "
            "attempts OCR via pytesseract+pdf2image (if installed). Reports clearly "
            "when proper OCR dependencies are needed."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "pdf_path": {
                    "type": "string",
                    "description": "Absolute path to the PDF file.",
                },
                "pages": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "Specific page numbers (1-indexed). Default: all pages.",
                },
                "language": {
                    "type": "string",
                    "description": "OCR language code (e.g. 'eng', 'fra', 'deu').",
                    "default": "eng",
                },
            },
            "required": ["pdf_path"],
        },
    ),
    Tool(
        name="pdf_to_images",
        description=(
            "Convert PDF pages to images. Tries pdf2image (Poppler) for full-page "
            "rendering. Falls back to extracting embedded images from each page using pypdf. "
            "Supports PNG and JPEG output formats."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "pdf_path": {
                    "type": "string",
                    "description": "Absolute path to the PDF file.",
                },
                "output_dir": {
                    "type": "string",
                    "description": "Directory where images will be saved.",
                },
                "format": {
                    "type": "string",
                    "enum": ["png", "jpeg"],
                    "description": "Output image format.",
                    "default": "png",
                },
                "dpi": {
                    "type": "integer",
                    "description": "Resolution in DPI for rendering (pdf2image only).",
                    "default": 150,
                    "minimum": 72,
                    "maximum": 600,
                },
                "pages": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "Specific page numbers (1-indexed). Default: all pages.",
                },
            },
            "required": ["pdf_path", "output_dir"],
        },
    ),
]

# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    return TOOLS


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        result = await _dispatch(name, arguments)
        return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
    except (FileNotFoundError, ValueError) as exc:
        error_payload = {"error": str(exc), "tool": name, "type": type(exc).__name__}
        return [TextContent(type="text", text=json.dumps(error_payload, indent=2))]
    except Exception as exc:
        error_payload = {
            "error": str(exc),
            "tool": name,
            "type": type(exc).__name__,
            "traceback": traceback.format_exc(),
        }
        return [TextContent(type="text", text=json.dumps(error_payload, indent=2))]


async def _dispatch(name: str, arguments: dict) -> dict:
    """Route tool calls to service functions."""

    if name == "merge_pdfs":
        return await merge_pdfs(
            pdf_paths=arguments["pdf_paths"],
            output_path=arguments["output_path"],
        )

    elif name == "split_pdf":
        return await split_pdf(
            pdf_path=arguments["pdf_path"],
            output_dir=arguments["output_dir"],
            mode=arguments["mode"],
            pages=arguments.get("pages"),
            ranges=arguments.get("ranges"),
            every_n=arguments.get("every_n"),
        )

    elif name == "extract_text":
        return await extract_text(
            pdf_path=arguments["pdf_path"],
            pages=arguments.get("pages"),
            format=arguments.get("format", "plain"),
        )

    elif name == "fill_form":
        return await fill_form(
            pdf_path=arguments["pdf_path"],
            output_path=arguments["output_path"],
            fields=arguments.get("fields"),
        )

    elif name == "add_watermark":
        return await add_watermark(
            pdf_path=arguments["pdf_path"],
            output_path=arguments["output_path"],
            text=arguments["text"],
            position=arguments.get("position", "diagonal"),
            opacity=arguments.get("opacity", 0.3),
            font_size=arguments.get("font_size", 40),
            color=arguments.get("color", "#808080"),
        )

    elif name == "pdf_ocr":
        return await pdf_ocr(
            pdf_path=arguments["pdf_path"],
            pages=arguments.get("pages"),
            language=arguments.get("language", "eng"),
        )

    elif name == "pdf_to_images":
        return await pdf_to_images(
            pdf_path=arguments["pdf_path"],
            output_dir=arguments["output_dir"],
            format=arguments.get("format", "png"),
            dpi=arguments.get("dpi", 150),
            pages=arguments.get("pages"),
        )

    else:
        raise ValueError(f"Unknown tool: '{name}'")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


async def _run():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


def main():
    asyncio.run(_run())


if __name__ == "__main__":
    main()
