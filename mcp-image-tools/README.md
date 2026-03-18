# MCP Image Tools

MCP server for production-grade image processing. 7 tools for resizing, converting, compressing, watermarking, metadata management, and batch processing.

**MCP Protocol** | **Python 3.11+** | **Pillow-based**

## Tools

### resize_image
Resize images with aspect ratio control. Supports lanczos, bilinear, bicubic, and nearest resampling. Provide width, height, or both -- when `maintain_aspect` is true and only one dimension is given, the other is calculated automatically.

### convert_format
Convert between PNG, JPEG, WebP, TIFF, BMP, GIF, and ICO. Automatically handles RGBA-to-RGB conversion for JPEG. Quality parameter controls lossy compression for JPEG/WebP.

### compress_image
Smart compression that detects format and applies the right strategy: JPEG quality + optimize, PNG optimize + compress_level, WebP quality + method 6. Optional max_width/max_height to downscale large images before compression.

### add_watermark
Text or image watermarks with positioning (center, corners, tile) and opacity control. Text watermarks auto-size based on image dimensions and include a shadow for readability. Image watermarks are auto-scaled to 1/4 of the base image. Tile mode repeats the watermark across the entire image.

### strip_metadata
Remove all EXIF, IPTC, XMP, and other metadata from images by creating a clean copy from pixel data. Optionally preserves ICC color profiles. Reports what metadata types were stripped.

### read_exif
Read and parse EXIF metadata into structured JSON. Returns camera make/model, date/time, exposure (shutter speed, f-stop, ISO), focal length, GPS coordinates (converted from DMS to decimal degrees), orientation, flash status, white balance, and metering mode.

### batch_process
Apply a pipeline of operations to all matching images in a directory. Supports chaining resize, convert, compress, strip_metadata, and watermark actions. Reports per-file success/failure status and total processing time.

## Installation

```bash
pip install -e .
```

## Usage with Claude Code

Add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "mcp-image-tools": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "/path/to/mcp-image-tools"
    }
  }
}
```

## Dependencies

- `mcp>=1.0.0` -- MCP protocol server
- `Pillow>=10.0.0` -- Image processing
- `pydantic>=2.0.0` -- Data validation

## License

Proprietary - All rights reserved.
