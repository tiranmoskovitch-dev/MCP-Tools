"""MCP Server: Compliance Report Generator
SOC2, HIPAA, GDPR, PCI-DSS automated evidence and reports
Price: $149
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.soc2_audit import register_soc2_audit
from src.tools.hipaa_check import register_hipaa_check
from src.tools.gdpr_assessment import register_gdpr_assessment
from src.tools.pci_scan import register_pci_scan
from src.tools.evidence_collect import register_evidence_collect
from src.tools.generate_report import register_generate_report
from src.tools.gap_analysis import register_gap_analysis

server = Server("mcp-compliance")


def register_all_tools():
    register_soc2_audit(server)
    register_hipaa_check(server)
    register_gdpr_assessment(server)
    register_pci_scan(server)
    register_evidence_collect(server)
    register_generate_report(server)
    register_gap_analysis(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
