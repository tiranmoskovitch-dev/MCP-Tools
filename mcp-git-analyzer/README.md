# Git Repository Analyzer

> Commit patterns, contributor stats, code churn, tech debt metrics

**Price:** $49 | **MCP Protocol** | **Python 3.11+**

## Tools

- **Repo Summary** — 
- **Contributor Stats** — 
- **Code Churn** — 
- **Commit Patterns** — 
- **File Hotspots** — 
- **Tech Debt Score** — 

## Installation

```bash
pip install -e .
```

## Usage with Claude Code

Add to your `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "mcp-git-analyzer": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "<path-to-mcp-git-analyzer>"
    }
  }
}
```

## License

Proprietary - All rights reserved.
