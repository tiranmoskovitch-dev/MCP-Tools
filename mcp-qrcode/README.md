# MCP QR Code Factory

Generate and decode QR codes, vCards, WiFi configs, and styled QR codes via the Model Context Protocol.

**MCP Protocol** | **Python 3.11+**

## Tools

### generate_qr
Generate a QR code from arbitrary text/URL data. Supports PNG and SVG output formats, configurable size, border, and error correction level. Returns base64-encoded image or saves to disk.

### decode_qr
Decode one or more QR codes from an image file or base64 data. Returns all decoded payloads with position rectangles and type information. Supports multiple QR codes in a single image.

### generate_vcard_qr
Generate a QR code containing a vCard 3.0 contact card. Provide name, email, phone, organization, title, URL, and address. Scan with a phone camera to add the contact instantly.

### generate_wifi_qr
Generate a QR code for WiFi network auto-connection. Supports WPA, WEP, and open networks. Handles hidden SSIDs. Scan to connect without typing a password.

### styled_qr
Generate a QR code with custom foreground/background colors and an optional logo embedded in the center. Uses high error correction (H) when a logo is present to maintain scannability.

### bulk_generate
Generate multiple QR codes in a single call. Provide a list of data items and an output directory. Filenames can be specified per-item or auto-generated from a data hash.

## Prerequisites

### System dependency: zbar

The `decode_qr` tool requires the **zbar** library for barcode/QR decoding.

- **Windows**: The `pyzbar` pip package bundles zbar DLLs — no extra install needed.
- **Linux (Debian/Ubuntu)**: `sudo apt-get install libzbar0`
- **Linux (Fedora)**: `sudo dnf install zbar`
- **macOS**: `brew install zbar`

If zbar is not installed, the `decode_qr` tool will return an informative error message. All other tools work without zbar.

## Installation

```bash
cd mcp-qrcode
pip install -e .
```

Or install dependencies directly:

```bash
pip install "mcp>=1.0.0" "qrcode[pil]>=7.4" "Pillow>=10.0.0" "pyzbar>=0.1.9" "pydantic>=2.0.0"
```

## Usage with Claude Code

Add to your `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "mcp-qrcode": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "/path/to/mcp-qrcode"
    }
  }
}
```

Or run directly:

```bash
python -m src.server
```

## File Structure

```
mcp-qrcode/
  src/
    __init__.py
    server.py            # MCP server — tool definitions + dispatch
    services/
      __init__.py
      generator.py       # QR generation (basic, vcard, wifi, styled, bulk)
      decoder.py         # QR decoding via pyzbar
  pyproject.toml
  README.md
  LICENSE
```

## License

Proprietary - All rights reserved.
