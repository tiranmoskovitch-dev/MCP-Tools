# Compliance Report Generator

> SOC2, HIPAA, GDPR, PCI-DSS automated evidence and reports

**Price:** $149 | **MCP Protocol** | **Python 3.11+**

## Tools

- **Soc2 Audit** — 
- **Hipaa Check** — 
- **Gdpr Assessment** — 
- **Pci Scan** — 
- **Evidence Collect** — 
- **Generate Report** — 
- **Gap Analysis** — 

## Installation

```bash
pip install -e .
```

## Usage with Claude Code

Add to your `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "mcp-compliance": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "<path-to-mcp-compliance>"
    }
  }
}
```

## License

Proprietary - All rights reserved.
