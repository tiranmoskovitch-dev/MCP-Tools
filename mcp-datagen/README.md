# Lorem & Data Generator

> Fake data generation: names, addresses, credit cards, UUIDs, datasets

**Price:** $29 | **MCP Protocol** | **Python 3.11+**

## Tools

- **Fake Person** — 
- **Fake Address** — 
- **Fake Company** — 
- **Fake Dataset** — 
- **Generate Uuids** — 
- **Fake Credit Card** — 

## Installation

```bash
pip install -e .
```

## Usage with Claude Code

Add to your `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "mcp-datagen": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "<path-to-mcp-datagen>"
    }
  }
}
```

## License

Proprietary - All rights reserved.
