# Dependency Auditor

> CVE scanning, license compliance, outdated deps, upgrade paths

**Price:** $49 | **MCP Protocol** | **Python 3.11+**

## Tools

- **Scan Vulnerabilities** — 
- **Check Licenses** — 
- **Find Outdated** — 
- **Upgrade Path** — 
- **Dependency Tree** — 
- **Audit Report** — 

## Installation

```bash
pip install -e .
```

## Usage with Claude Code

Add to your `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "mcp-dep-audit": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "<path-to-mcp-dep-audit>"
    }
  }
}
```

## License

Proprietary - All rights reserved.
