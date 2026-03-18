# Data Quality Monitor

> Anomaly detection, missing data patterns, schema drift, profiling

**Price:** $79 | **MCP Protocol** | **Python 3.11+**

## Tools

- **Profile Dataset** — 
- **Detect Anomalies** — 
- **Check Completeness** — 
- **Schema Drift** — 
- **Quality Score** — 
- **Validation Rules** — 

## Installation

```bash
pip install -e .
```

## Usage with Claude Code

Add to your `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "mcp-data-quality": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "<path-to-mcp-data-quality>"
    }
  }
}
```

## License

Proprietary - All rights reserved.
