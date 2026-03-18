"""MCP Server: API Security Scanner
OWASP top 10 testing, auth bypass detection, injection scanning
Price: $79
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.scan_owasp import register_scan_owasp
from src.tools.test_auth import register_test_auth
from src.tools.injection_test import register_injection_test
from src.tools.rate_limit_test import register_rate_limit_test
from src.tools.cors_check import register_cors_check
from src.tools.security_report import register_security_report

server = Server("mcp-api-security")


def register_all_tools():
    register_scan_owasp(server)
    register_test_auth(server)
    register_injection_test(server)
    register_rate_limit_test(server)
    register_cors_check(server)
    register_security_report(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
