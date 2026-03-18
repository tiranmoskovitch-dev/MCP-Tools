"""MCP Server: DNS & Domain Intelligence
WHOIS lookup, DNS records, subdomain enumeration, SSL certificate analysis.
"""
import asyncio
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from src.services import (
    whois_lookup,
    dns_records,
    subdomain_enum,
    ssl_cert_info,
    reverse_dns,
    domain_age,
)

server = Server("mcp-dns-intel")

TOOLS = [
    Tool(
        name="whois_lookup",
        description=(
            "Perform a WHOIS lookup on a domain. Returns registrar, creation/expiration dates, "
            "name servers, registration status, registrant info, and DNSSEC status."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "domain": {
                    "type": "string",
                    "description": "The domain name to look up (e.g. 'example.com')",
                },
            },
            "required": ["domain"],
        },
    ),
    Tool(
        name="dns_records",
        description=(
            "Query DNS records for a domain. Supports A, AAAA, MX, NS, TXT, CNAME, SOA, CAA, SRV, PTR. "
            "Returns structured results with TTL and record-specific parsed fields."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "domain": {
                    "type": "string",
                    "description": "The domain name to query (e.g. 'example.com')",
                },
                "record_type": {
                    "type": "string",
                    "description": "DNS record type to query: A, AAAA, MX, NS, TXT, CNAME, SOA, CAA, SRV, PTR, or ALL (default: ALL)",
                    "default": "ALL",
                },
            },
            "required": ["domain"],
        },
    ),
    Tool(
        name="subdomain_enum",
        description=(
            "Enumerate subdomains of a domain using async DNS brute-force with a built-in wordlist "
            "of 100 common subdomains. Returns discovered subdomains with their A record IPs."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "domain": {
                    "type": "string",
                    "description": "The base domain to enumerate subdomains for (e.g. 'example.com')",
                },
                "wordlist": {
                    "type": "string",
                    "description": "Wordlist to use: 'common' (default, 100 entries)",
                    "default": "common",
                },
            },
            "required": ["domain"],
        },
    ),
    Tool(
        name="ssl_cert_info",
        description=(
            "Inspect the SSL/TLS certificate of a domain. Returns subject, issuer, validity dates, "
            "days until expiry, signature algorithm, public key info, SANs, chain info, and expiry status."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "domain": {
                    "type": "string",
                    "description": "The domain to inspect the SSL certificate for (e.g. 'example.com')",
                },
                "port": {
                    "type": "integer",
                    "description": "The port to connect to (default: 443)",
                    "default": 443,
                },
            },
            "required": ["domain"],
        },
    ),
    Tool(
        name="reverse_dns",
        description=(
            "Perform a reverse DNS (PTR) lookup on an IP address. Verifies forward-confirmed reverse DNS "
            "by resolving the PTR hostname back and checking if it matches the original IP."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "ip": {
                    "type": "string",
                    "description": "The IP address to look up (e.g. '8.8.8.8')",
                },
            },
            "required": ["ip"],
        },
    ),
    Tool(
        name="domain_age",
        description=(
            "Calculate the age of a domain from WHOIS creation date. Returns age in years/months/days, "
            "expiration info, registrar, and whether the domain is newly registered (< 30 days)."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "domain": {
                    "type": "string",
                    "description": "The domain name to check age for (e.g. 'example.com')",
                },
            },
            "required": ["domain"],
        },
    ),
]

HANDLERS = {
    "whois_lookup": whois_lookup,
    "dns_records": dns_records,
    "subdomain_enum": subdomain_enum,
    "ssl_cert_info": ssl_cert_info,
    "reverse_dns": reverse_dns,
    "domain_age": domain_age,
}


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    return TOOLS


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[TextContent]:
    handler = HANDLERS.get(name)
    if handler is None:
        return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]

    arguments = arguments or {}
    try:
        result = await handler(**arguments)
    except Exception as exc:
        result = {"error": str(exc), "error_type": type(exc).__name__}

    return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]


async def run():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
