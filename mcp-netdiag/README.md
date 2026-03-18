# Network Diagnostics

> Ping, traceroute, port scan, SSL check, HTTP header analysis

**Price:** $29 | **MCP Protocol** | **Python 3.11+**

## Tools

- **Ping Host** — 
- **Traceroute** — 
- **Port Scan** — 
- **Ssl Check** — 
- **Http Headers** — 
- **Dns Lookup** — 

## Installation

```bash
pip install -e .
```

## Usage with Claude Code

Add to your `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "mcp-netdiag": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "<path-to-mcp-netdiag>"
    }
  }
}
```

## License

Proprietary - All rights reserved.
