# Stock Sentiment Analyzer

> Earnings call NLP, insider trades, options flow, SEC filing parser

**Price:** $79 | **MCP Protocol** | **Python 3.11+**

## Tools

- **Analyze Earnings** — 
- **Insider Trades** — 
- **Options Flow** — 
- **Sec Filings** — 
- **News Sentiment** — 
- **Analyst Ratings** — 

## Installation

```bash
pip install -e .
```

## Usage with Claude Code

Add to your `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "mcp-stock-sentiment": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "<path-to-mcp-stock-sentiment>"
    }
  }
}
```

## License

Proprietary - All rights reserved.
