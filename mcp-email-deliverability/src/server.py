import asyncio
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server

server = Server("mcp-email-deliverability")

TOOLS = [
    {
        "name": "check_spf",
        "description": "Check SPF (Sender Policy Framework) record for a domain. Parses the SPF TXT record, extracts all mechanisms (ip4, ip6, include, a, mx, redirect, all), evaluates the policy strength, and identifies configuration issues.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {
                    "type": "string",
                    "description": "Domain name to check SPF record for (e.g. 'example.com')",
                }
            },
            "required": ["domain"],
        },
    },
    {
        "name": "check_dkim",
        "description": "Check DKIM (DomainKeys Identified Mail) record for a domain. Looks up the DKIM TXT record at {selector}._domainkey.{domain}, parses key fields, determines key type and bit length, and validates the configuration.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {
                    "type": "string",
                    "description": "Domain name to check DKIM record for",
                },
                "selector": {
                    "type": "string",
                    "description": "DKIM selector to check (default: 'default'). Common selectors: google, selector1, selector2, s1, s2, dkim, mail",
                    "default": "default",
                },
            },
            "required": ["domain"],
        },
    },
    {
        "name": "check_dmarc",
        "description": "Check DMARC (Domain-based Message Authentication, Reporting & Conformance) record for a domain. Parses all DMARC tags (v, p, sp, rua, ruf, adkim, aspf, pct, fo, rf, ri), analyzes enforcement level, reporting configuration, alignment mode, and provides recommendations.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {
                    "type": "string",
                    "description": "Domain name to check DMARC record for",
                }
            },
            "required": ["domain"],
        },
    },
    {
        "name": "spam_score",
        "description": "Calculate a 0-100 email deliverability score for a domain. Runs comprehensive checks (SPF, DKIM with common selectors, DMARC, MX records, reverse DNS) and calculates a weighted score with grade (A-F), detailed breakdown of deductions, and actionable recommendations.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {
                    "type": "string",
                    "description": "Domain name to score for email deliverability",
                }
            },
            "required": ["domain"],
        },
    },
    {
        "name": "domain_reputation",
        "description": "Check domain email reputation. Analyzes MX records and identifies mail providers, checks primary MX IP against DNS blacklists (Spamhaus, SpamCop, Barracuda, SORBS), retrieves SOA and nameserver information, and provides an overall reputation assessment.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {
                    "type": "string",
                    "description": "Domain name to check reputation for",
                }
            },
            "required": ["domain"],
        },
    },
    {
        "name": "validate_email",
        "description": "Validate an email address. Checks RFC 5322 format compliance, verifies the domain has MX records, detects disposable/temporary email domains (50+ known providers), and identifies role-based addresses (admin@, info@, support@, etc). Returns a risk level assessment.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "description": "Email address to validate (e.g. 'user@example.com')",
                }
            },
            "required": ["email"],
        },
    },
]

HANDLERS = {}


def _register_handlers():
    from src.services.dns_checks import check_spf, check_dkim, check_dmarc
    from src.services.scoring import calculate_spam_score
    from src.services.reputation import check_domain_reputation
    from src.services.validation import validate_email

    async def handle_check_spf(args):
        return await check_spf(args["domain"])

    async def handle_check_dkim(args):
        return await check_dkim(args["domain"], args.get("selector", "default"))

    async def handle_check_dmarc(args):
        return await check_dmarc(args["domain"])

    async def handle_spam_score(args):
        return await calculate_spam_score(args["domain"])

    async def handle_domain_reputation(args):
        return await check_domain_reputation(args["domain"])

    async def handle_validate_email(args):
        return await validate_email(args["email"])

    HANDLERS["check_spf"] = handle_check_spf
    HANDLERS["check_dkim"] = handle_check_dkim
    HANDLERS["check_dmarc"] = handle_check_dmarc
    HANDLERS["spam_score"] = handle_spam_score
    HANDLERS["domain_reputation"] = handle_domain_reputation
    HANDLERS["validate_email"] = handle_validate_email


@server.list_tools()
async def list_tools():
    from mcp.types import Tool
    return [Tool(**t) for t in TOOLS]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    from mcp.types import TextContent

    if not HANDLERS:
        _register_handlers()

    handler = HANDLERS.get(name)
    if not handler:
        return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]

    try:
        result = await handler(arguments)
        return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e), "tool": name}))]


async def run():
    _register_handlers()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
