# API Load Tester

> HTTP benchmarking, concurrent requests, latency percentiles, reports

**Price:** $49 | **MCP Protocol** | **Python 3.11+**

## Tools

- **Run Benchmark** — 
- **Concurrent Test** — 
- **Stress Test** — 
- **Latency Report** — 
- **Compare Endpoints** — 
- **Export Results** — 

## Installation

```bash
pip install -e .
```

## Usage with Claude Code

Add to your `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "mcp-loadtest": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "<path-to-mcp-loadtest>"
    }
  }
}
```

## License

Proprietary - All rights reserved.
