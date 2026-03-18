"""MCP Server: Vulnerability Manager
CVE tracking, asset inventory, patch prioritization, exploits
Price: $99
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.scan_assets import register_scan_assets
from src.tools.track_cves import register_track_cves
from src.tools.prioritize_patches import register_prioritize_patches
from src.tools.exploit_check import register_exploit_check
from src.tools.remediation_plan import register_remediation_plan
from src.tools.vuln_report import register_vuln_report

server = Server("mcp-vuln-manager")


def register_all_tools():
    register_scan_assets(server)
    register_track_cves(server)
    register_prioritize_patches(server)
    register_exploit_check(server)
    register_remediation_plan(server)
    register_vuln_report(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
