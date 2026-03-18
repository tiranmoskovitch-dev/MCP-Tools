"""MCP Server: Smart Contract Auditor
Solidity analysis, gas optimization, vulnerability patterns
Price: $79
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.analyze_contract import register_analyze_contract
from src.tools.gas_optimize import register_gas_optimize
from src.tools.find_vulnerabilities import register_find_vulnerabilities
from src.tools.reentrancy_check import register_reentrancy_check
from src.tools.access_control import register_access_control
from src.tools.audit_report import register_audit_report

server = Server("mcp-contract-audit")


def register_all_tools():
    register_analyze_contract(server)
    register_gas_optimize(server)
    register_find_vulnerabilities(server)
    register_reentrancy_check(server)
    register_access_control(server)
    register_audit_report(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
