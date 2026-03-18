<!-- DEVGUARD:START -->
# DevGuard Rules (auto-generated)

## Mandatory (P0)
- NEVER use placeholder data, fake values, or TODO comments in production code
- NEVER hardcode secrets, API keys, passwords, or credentials
- ALWAYS ask before making assumptions about requirements
- ALWAYS verify with the user before using mock/sample data

## Strong Preference (P1)
- Ask all clarifying questions BEFORE starting implementation
- If using placeholder data temporarily, register it immediately
- Run DevGuard scan before considering any task complete

## Default (P2)
- Prefer coded/scripted processes over AI-generated actions for repeatable tasks
- Create checkpoint after completing each logical unit of work
- Keep session blueprint updated with any scope changes

<!-- DEVGUARD:END -->

---

# MCP-Tools — Project Context

## What This Project Is
A collection of 50 MCP (Model Context Protocol) servers being built over 12 weeks.
Each tool is a standalone Python server that gives Claude Code (or any AI tool)
new abilities — like checking DNS records, generating QR codes, or auditing PDFs.

These are products for sale on Whop ($29-$149 each).

## Schedule
- Full schedule: `SCHEDULE.md`
- 53 tool directories exist, 5 validated and ready for sale (Week 1 complete)
- Scaffold tool: `python scaffold.py <tool-name>` creates a new tool from template

## Completed Tools (Week 1)
| Tool | Price | What It Does |
|------|-------|-------------|
| `mcp-email-deliverability` | $29 | Checks if email setup is correct (SPF, DKIM, DMARC, spam score) |
| `mcp-dns-intel` | $29 | Looks up domain info (WHOIS, DNS records, SSL certificates) |
| `mcp-qrcode` | $29 | Creates and reads QR codes, including styled/branded ones |
| `mcp-pdf-toolkit` | $29 | Merges, splits, OCRs, and watermarks PDF files |
| `mcp-image-tools` | $29 | Resizes, converts, compresses images, reads EXIF data |

## How Each Tool Is Structured
Every tool follows the same pattern:
```
mcp-<name>/
  src/
    server.py    # Main MCP server — tool definitions and handlers
    __init__.py
  tests/
    test_*.py    # pytest tests
  pyproject.toml # Package config
  README.md
```

## How to Run a Tool
```bash
cd mcp-<name>
pip install -e .
python -m src.server           # stdio mode (for Claude Code)
python -m src.server --http    # HTTP mode (for web clients)
```

## How to Create a New Tool
```bash
python scaffold.py mcp-new-tool-name
# Then implement the tools in src/server.py
```

## Revenue Target
- 50 tools total = $3,014 at 1 sale each
- 4 bundles = +$1,646
- Grand total potential: $4,660

## Rules for This Project
- Each tool must be fully self-contained — no shared dependencies between tools
- Every tool needs tests in `tests/` — run with `pytest`
- Whop listings text is in `whop-listings.md` — keep it updated when tools change
- Price tiers: $29 (basic), $49 (intermediate), $79 (advanced), $99-149 (enterprise)
- The scaffold creates the right structure — always use it for new tools
