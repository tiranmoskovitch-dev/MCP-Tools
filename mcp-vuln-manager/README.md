# Vulnerability Manager

> CVE tracking, asset inventory, patch prioritization, exploits

**Price:** $99 | **MCP Protocol** | **Python 3.11+**

## Tools

- **Scan Assets** — 
- **Track Cves** — 
- **Prioritize Patches** — 
- **Exploit Check** — 
- **Remediation Plan** — 
- **Vuln Report** — 

## Installation

```bash
pip install -e .
```

## Usage with Claude Code

Add to your `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "mcp-vuln-manager": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "<path-to-mcp-vuln-manager>"
    }
  }
}
```

## License

Proprietary - All rights reserved.
