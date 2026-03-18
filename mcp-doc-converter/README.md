# Markdown & Doc Converter

> Convert between MD, HTML, PDF, DOCX, RST with table formatting

**Price:** $29 | **MCP Protocol** | **Python 3.11+**

## Tools

- **Md To Html** — 
- **Md To Pdf** — 
- **Html To Md** — 
- **Docx To Md** — 
- **Generate Toc** — 
- **Format Tables** — 

## Installation

```bash
pip install -e .
```

## Usage with Claude Code

Add to your `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "mcp-doc-converter": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "<path-to-mcp-doc-converter>"
    }
  }
}
```

## License

Proprietary - All rights reserved.
