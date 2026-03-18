# SEO Site Auditor

> Crawl site, Core Web Vitals, structured data, broken links

**Price:** $49 | **MCP Protocol** | **Python 3.11+**

## Tools

- **Crawl Site** — 
- **Check Vitals** — 
- **Validate Schema** — 
- **Find Broken Links** — 
- **Check Sitemap** — 
- **Seo Score** — 

## Installation

```bash
pip install -e .
```

## Usage with Claude Code

Add to your `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "mcp-seo-audit": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "<path-to-mcp-seo-audit>"
    }
  }
}
```

## License

Proprietary - All rights reserved.
