"""MCP Server: Dependency Auditor
CVE scanning, license compliance, outdated deps, upgrade paths
Price: $49
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.scan_vulnerabilities import register_scan_vulnerabilities
from src.tools.check_licenses import register_check_licenses
from src.tools.find_outdated import register_find_outdated
from src.tools.upgrade_path import register_upgrade_path
from src.tools.dependency_tree import register_dependency_tree
from src.tools.audit_report import register_audit_report

server = Server("mcp-dep-audit")


def register_all_tools():
    register_scan_vulnerabilities(server)
    register_check_licenses(server)
    register_find_outdated(server)
    register_upgrade_path(server)
    register_dependency_tree(server)
    register_audit_report(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
