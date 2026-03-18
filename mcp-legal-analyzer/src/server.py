"""MCP Server: Legal Document Analyzer
Contract clause extraction, risk flags, NDA comparison
Price: $79
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.extract_clauses import register_extract_clauses
from src.tools.risk_analysis import register_risk_analysis
from src.tools.compare_contracts import register_compare_contracts
from src.tools.nda_review import register_nda_review
from src.tools.compliance_check import register_compliance_check
from src.tools.summary_report import register_summary_report

server = Server("mcp-legal-analyzer")


def register_all_tools():
    register_extract_clauses(server)
    register_risk_analysis(server)
    register_compare_contracts(server)
    register_nda_review(server)
    register_compliance_check(server)
    register_summary_report(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
