# AWS Cost Optimizer

> Resource waste detection, reserved instance recommendations, savings

**Price:** $49 | **MCP Protocol** | **Python 3.11+**

## Tools

- **Cost Breakdown** — 
- **Waste Detection** — 
- **Ri Recommendations** — 
- **Savings Plan** — 
- **Forecast Costs** — 
- **Tag Audit** — 

## Installation

```bash
pip install -e .
```

## Usage with Claude Code

Add to your `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "mcp-aws-costs": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "<path-to-mcp-aws-costs>"
    }
  }
}
```

## License

Proprietary - All rights reserved.
