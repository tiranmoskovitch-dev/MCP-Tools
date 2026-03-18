"""MCP Server: Crypto Portfolio Tracker
Multi-exchange portfolio, DeFi tracking, tax reporting, P&L
Price: $79
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.portfolio_summary import register_portfolio_summary
from src.tools.track_exchange import register_track_exchange
from src.tools.defi_positions import register_defi_positions
from src.tools.tax_report import register_tax_report
from src.tools.pnl_analysis import register_pnl_analysis
from src.tools.whale_alerts import register_whale_alerts

server = Server("mcp-crypto-portfolio")


def register_all_tools():
    register_portfolio_summary(server)
    register_track_exchange(server)
    register_defi_positions(server)
    register_tax_report(server)
    register_pnl_analysis(server)
    register_whale_alerts(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
