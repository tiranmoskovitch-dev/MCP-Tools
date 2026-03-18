"""MCP Server: Network Diagnostics
Ping, traceroute, port scan, SSL check, HTTP header analysis
Price: $29
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.ping_host import register_ping_host
from src.tools.traceroute import register_traceroute
from src.tools.port_scan import register_port_scan
from src.tools.ssl_check import register_ssl_check
from src.tools.http_headers import register_http_headers
from src.tools.dns_lookup import register_dns_lookup

server = Server("mcp-netdiag")


def register_all_tools():
    register_ping_host(server)
    register_traceroute(server)
    register_port_scan(server)
    register_ssl_check(server)
    register_http_headers(server)
    register_dns_lookup(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
