# Data Pipeline Orchestrator

> ETL workflows, scheduling, monitoring, retry logic, lineage

**Price:** $99 | **MCP Protocol** | **Python 3.11+**

## Tools

- **Create Pipeline** — 
- **Run Pipeline** — 
- **Monitor Jobs** — 
- **Retry Failed** — 
- **Data Lineage** — 
- **Schedule Pipeline** — 
- **Pipeline Stats** — 

## Installation

```bash
pip install -e .
```

## Usage with Claude Code

Add to your `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "mcp-data-pipeline": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "<path-to-mcp-data-pipeline>"
    }
  }
}
```

## License

Proprietary - All rights reserved.
