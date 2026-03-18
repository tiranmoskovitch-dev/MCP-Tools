# MCP PDF Toolkit

Production-grade MCP server providing seven PDF manipulation tools. Built on pypdf, pdfplumber, reportlab, and Pillow.

## Tools

| Tool | Description |
|------|-------------|
| `merge_pdfs` | Merge multiple PDFs into one output file |
| `split_pdf` | Split a PDF by specific pages, ranges, or every-N chunks |
| `extract_text` | Extract text from PDF pages (plain or structured with layout info) |
| `fill_form` | List available form fields or fill them with provided values |
| `add_watermark` | Overlay text watermark on every page (center/diagonal/header/footer) |
| `pdf_ocr` | Extract text with OCR fallback for scanned documents |
| `pdf_to_images` | Convert PDF pages to PNG/JPEG images |

## Installation

```bash
pip install -e .
```

### Optional dependencies

```bash
# For true OCR on scanned PDFs
pip install pytesseract pdf2image
# Also requires Tesseract binary and Poppler binaries on system PATH

# For full-page PDF rendering to images (instead of embedded image extraction)
pip install pdf2image
# Requires Poppler binaries on system PATH
```

## Dependencies

| Package | Purpose |
|---------|---------|
| `mcp>=1.0.0` | MCP protocol server framework |
| `pypdf>=4.0.0` | PDF reading, writing, merging, splitting, form filling |
| `pdfplumber>=0.11.0` | High-quality text extraction with layout info |
| `reportlab>=4.1.0` | Watermark PDF page generation |
| `Pillow>=10.0.0` | Image processing for PDF-to-image conversion |
| `pydantic>=2.0.0` | Data validation |

## Usage

### As an MCP server (stdio transport)

```bash
mcp-pdf-toolkit
# or
python -m src.server
```

### Claude Desktop / Claude Code configuration

```json
{
  "mcpServers": {
    "pdf-toolkit": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "E:/MCP-Tools/mcp-pdf-toolkit"
    }
  }
}
```

## Tool Details

### merge_pdfs

Combine multiple PDFs into a single file. Pages are appended in the order of the input list.

**Input:** `pdf_paths` (list of strings), `output_path` (string)
**Returns:** output_path, total_pages, source_files count

### split_pdf

Split a PDF using one of three modes:
- **pages**: Extract specific page numbers (e.g., pages 1, 3, 5)
- **ranges**: Extract page ranges (e.g., "1-3,5-7")
- **every_n**: Split into chunks of N pages

**Input:** `pdf_path`, `output_dir`, `mode`, plus mode-specific params (`pages`, `ranges`, `every_n`)
**Returns:** list of output files with page counts

### extract_text

Extract text from PDF pages using pdfplumber. Two formats:
- **plain**: Raw text per page
- **structured**: Text with bounding boxes, font names, font sizes, and detected tables

**Input:** `pdf_path`, optional `pages`, optional `format`
**Returns:** text content per page, total_pages, total_chars

### fill_form

Inspect or fill PDF form fields:
- **Listing mode** (no `fields` provided): Returns all form fields with types and current values
- **Fill mode** (`fields` provided): Fills specified fields and saves output

**Input:** `pdf_path`, `output_path`, optional `fields` dict
**Returns:** filled field count, output_path, available_fields

### add_watermark

Overlay text watermark on every page. Creates a transparent watermark page with reportlab, then merges it onto each source page.

**Input:** `pdf_path`, `output_path`, `text`, optional `position`/`opacity`/`font_size`/`color`
**Returns:** output_path, pages_watermarked

### pdf_ocr

Text extraction with OCR fallback:
1. Primary: pdfplumber text extraction
2. If very little text found and pytesseract+pdf2image are installed: OCR via Tesseract
3. If OCR deps missing: returns extracted text with guidance on installing OCR dependencies

**Input:** `pdf_path`, optional `pages`, optional `language`
**Returns:** text per page, extraction_method, confidence note

### pdf_to_images

Convert PDF pages to images:
1. Primary: pdf2image with Poppler (full page rendering at specified DPI)
2. Fallback: Extract embedded images from each page using pypdf

**Input:** `pdf_path`, `output_dir`, optional `format`/`dpi`/`pages`
**Returns:** list of output image paths, method used

## Architecture

```
src/
  server.py          # MCP server: tool definitions + dispatch
  services/
    merger.py        # merge_pdfs implementation
    splitter.py      # split_pdf implementation
    extractor.py     # extract_text + pdf_ocr implementations
    forms.py         # fill_form implementation
    watermark.py     # add_watermark implementation
    converter.py     # pdf_to_images implementation
```

Single `@server.list_tools()` and `@server.call_tool()` with dispatch to service functions. All tools return structured JSON. Encrypted/corrupted PDFs are handled gracefully with clear error messages.

## License

MIT
