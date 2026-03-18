"""MCP Server: Image Processing Tools
Resize, convert, compress, watermark, metadata strip, EXIF read, batch process.
"""
import asyncio
import json
import traceback

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from src.services.resize import resize_image
from src.services.convert import convert_format
from src.services.compress import compress_image
from src.services.watermark import add_watermark
from src.services.metadata import strip_metadata, read_exif
from src.services.batch import batch_process

server = Server("mcp-image-tools")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="resize_image",
            description="Resize an image to specified dimensions. Can maintain aspect ratio by providing only width or height. Supports lanczos, bilinear, bicubic, and nearest resampling.",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the input image file",
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Path for the output file. If not provided, overwrites the input file.",
                    },
                    "width": {
                        "type": "integer",
                        "description": "Target width in pixels",
                    },
                    "height": {
                        "type": "integer",
                        "description": "Target height in pixels",
                    },
                    "maintain_aspect": {
                        "type": "boolean",
                        "description": "Maintain aspect ratio when resizing (default: true)",
                        "default": True,
                    },
                    "resample": {
                        "type": "string",
                        "enum": ["lanczos", "bilinear", "bicubic", "nearest"],
                        "description": "Resampling filter to use (default: lanczos)",
                        "default": "lanczos",
                    },
                },
                "required": ["image_path"],
            },
        ),
        Tool(
            name="convert_format",
            description="Convert an image to a different format (PNG, JPEG, WebP, TIFF, BMP, GIF, ICO). Handles RGBA to RGB conversion for JPEG automatically.",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the input image file",
                    },
                    "output_format": {
                        "type": "string",
                        "enum": ["png", "jpeg", "webp", "tiff", "bmp", "gif", "ico"],
                        "description": "Target image format",
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Path for the output file. If not provided, uses input path with new extension.",
                    },
                    "quality": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 100,
                        "description": "Quality for lossy formats like JPEG and WebP (default: 85)",
                        "default": 85,
                    },
                },
                "required": ["image_path", "output_format"],
            },
        ),
        Tool(
            name="compress_image",
            description="Smart image compression. Detects format and applies appropriate compression: JPEG quality, PNG optimize+compress_level, WebP quality. Can also downscale if max dimensions are specified.",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the input image file",
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Path for the output file. If not provided, overwrites the input file.",
                    },
                    "quality": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 100,
                        "description": "Compression quality 1-100 (default: 75)",
                        "default": 75,
                    },
                    "max_width": {
                        "type": "integer",
                        "description": "Maximum width — image will be downscaled if wider",
                    },
                    "max_height": {
                        "type": "integer",
                        "description": "Maximum height — image will be downscaled if taller",
                    },
                    "format": {
                        "type": "string",
                        "description": "Output format if different from input (e.g. 'webp')",
                    },
                },
                "required": ["image_path"],
            },
        ),
        Tool(
            name="add_watermark",
            description="Add a text or image watermark to an image. Supports positioning (center, corners, tile) and opacity control. Text watermarks include a shadow for readability.",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the input image file",
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Path for the output file. If not provided, overwrites the input file.",
                    },
                    "text": {
                        "type": "string",
                        "description": "Text to use as watermark",
                    },
                    "watermark_image_path": {
                        "type": "string",
                        "description": "Path to a watermark image to overlay",
                    },
                    "position": {
                        "type": "string",
                        "enum": ["center", "bottom-right", "bottom-left", "top-right", "top-left", "tile"],
                        "description": "Watermark position (default: bottom-right)",
                        "default": "bottom-right",
                    },
                    "opacity": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1,
                        "description": "Watermark opacity 0.0-1.0 (default: 0.5)",
                        "default": 0.5,
                    },
                    "font_size": {
                        "type": "integer",
                        "description": "Font size for text watermarks. Auto-calculated based on image size if not provided.",
                    },
                },
                "required": ["image_path"],
            },
        ),
        Tool(
            name="strip_metadata",
            description="Remove all metadata (EXIF, IPTC, XMP, etc.) from an image. Creates a clean image from pixel data only. Can optionally preserve ICC color profile.",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the input image file",
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Path for the output file. If not provided, overwrites the input file.",
                    },
                    "keep_icc": {
                        "type": "boolean",
                        "description": "Keep ICC color profile (default: true)",
                        "default": True,
                    },
                },
                "required": ["image_path"],
            },
        ),
        Tool(
            name="read_exif",
            description="Read EXIF metadata from an image. Returns structured data including camera make/model, date/time, exposure settings, GPS coordinates (converted to decimal degrees), orientation, flash, white balance, and metering mode.",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the image file to read EXIF from",
                    },
                    "include_thumbnail": {
                        "type": "boolean",
                        "description": "Include embedded thumbnail data (default: false)",
                        "default": False,
                    },
                },
                "required": ["image_path"],
            },
        ),
        Tool(
            name="batch_process",
            description="Apply a sequence of image operations to all matching images in a directory. Supported actions: resize, convert, compress, strip_metadata, watermark. Processes files sequentially and reports per-file status.",
            inputSchema={
                "type": "object",
                "properties": {
                    "input_dir": {
                        "type": "string",
                        "description": "Directory containing input images",
                    },
                    "output_dir": {
                        "type": "string",
                        "description": "Directory for processed output images",
                    },
                    "operations": {
                        "type": "array",
                        "description": "List of operations to apply sequentially to each image",
                        "items": {
                            "type": "object",
                            "properties": {
                                "action": {
                                    "type": "string",
                                    "enum": ["resize", "convert", "compress", "strip_metadata", "watermark"],
                                    "description": "The operation to perform",
                                },
                            },
                            "required": ["action"],
                        },
                    },
                    "pattern": {
                        "type": "string",
                        "description": "Glob pattern for matching image files (default: '*.{jpg,jpeg,png,webp,gif,bmp,tiff}')",
                        "default": "*.{jpg,jpeg,png,webp,gif,bmp,tiff}",
                    },
                },
                "required": ["input_dir", "output_dir", "operations"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        result = _dispatch(name, arguments)
        return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
    except Exception as e:
        error_info = {
            "error": str(e),
            "tool": name,
            "traceback": traceback.format_exc(),
        }
        return [TextContent(type="text", text=json.dumps(error_info, indent=2))]


def _dispatch(name: str, args: dict) -> dict:
    if name == "resize_image":
        return resize_image(
            image_path=args["image_path"],
            output_path=args.get("output_path"),
            width=args.get("width"),
            height=args.get("height"),
            maintain_aspect=args.get("maintain_aspect", True),
            resample=args.get("resample", "lanczos"),
        )

    elif name == "convert_format":
        return convert_format(
            image_path=args["image_path"],
            output_format=args["output_format"],
            output_path=args.get("output_path"),
            quality=args.get("quality", 85),
        )

    elif name == "compress_image":
        return compress_image(
            image_path=args["image_path"],
            output_path=args.get("output_path"),
            quality=args.get("quality", 75),
            max_width=args.get("max_width"),
            max_height=args.get("max_height"),
            format=args.get("format"),
        )

    elif name == "add_watermark":
        return add_watermark(
            image_path=args["image_path"],
            output_path=args.get("output_path"),
            text=args.get("text"),
            watermark_image_path=args.get("watermark_image_path"),
            position=args.get("position", "bottom-right"),
            opacity=args.get("opacity", 0.5),
            font_size=args.get("font_size"),
        )

    elif name == "strip_metadata":
        return strip_metadata(
            image_path=args["image_path"],
            output_path=args.get("output_path"),
            keep_icc=args.get("keep_icc", True),
        )

    elif name == "read_exif":
        return read_exif(
            image_path=args["image_path"],
            include_thumbnail=args.get("include_thumbnail", False),
        )

    elif name == "batch_process":
        return batch_process(
            input_dir=args["input_dir"],
            output_dir=args["output_dir"],
            operations=args["operations"],
            pattern=args.get("pattern", "*.{jpg,jpeg,png,webp,gif,bmp,tiff}"),
        )

    else:
        raise ValueError(f"Unknown tool: {name}")


async def run():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
