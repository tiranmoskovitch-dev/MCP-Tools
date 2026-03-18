# Invoice & Receipt OCR

> Extract data from invoices/receipts, categorize expenses, export

**Price:** $49 | **MCP Protocol** | **Python 3.11+**

## Tools

- **Extract Invoice** — 
- **Extract Receipt** — 
- **Categorize Expense** — 
- **Batch Process** — 
- **Export Csv** — 
- **Tax Summary** — 

## Installation

```bash
pip install -e .
```

## Usage with Claude Code

Add to your `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "mcp-invoice-ocr": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "<path-to-mcp-invoice-ocr>"
    }
  }
}
```

## License

Proprietary - All rights reserved.
