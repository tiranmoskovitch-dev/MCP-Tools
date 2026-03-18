# Webhook Tester & Logger

> Receive, log, replay webhooks, mock API responses

**Price:** $29 | **MCP Protocol** | **Python 3.11+**

## Tools

- **Create Endpoint** — 
- **List Requests** — 
- **Replay Request** — 
- **Mock Response** — 
- **Webhook Stats** — 
- **Export Logs** — 

## Installation

```bash
pip install -e .
```

## Usage with Claude Code

Add to your `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "mcp-webhook": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "<path-to-mcp-webhook>"
    }
  }
}
```

## License

Proprietary - All rights reserved.
