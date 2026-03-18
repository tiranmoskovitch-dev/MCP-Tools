"""MCP Server: Cloud Security Auditor
IAM audit, misconfiguration detection, compliance gap mapping
Price: $79
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.iam_audit import register_iam_audit
from src.tools.misconfig_scan import register_misconfig_scan
from src.tools.compliance_check import register_compliance_check
from src.tools.network_exposure import register_network_exposure
from src.tools.encryption_audit import register_encryption_audit
from src.tools.security_score import register_security_score

server = Server("mcp-cloud-security")


def register_all_tools():
    register_iam_audit(server)
    register_misconfig_scan(server)
    register_compliance_check(server)
    register_network_exposure(server)
    register_encryption_audit(server)
    register_security_score(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
