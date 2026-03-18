"""MCP Server: Real Estate Analyzer
ROI calculation, market comparables, rental yield, neighborhood data
Price: $99
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.calculate_roi import register_calculate_roi
from src.tools.find_comparables import register_find_comparables
from src.tools.rental_yield import register_rental_yield
from src.tools.neighborhood_analysis import register_neighborhood_analysis
from src.tools.mortgage_calc import register_mortgage_calc
from src.tools.investment_report import register_investment_report

server = Server("mcp-real-estate")


def register_all_tools():
    register_calculate_roi(server)
    register_find_comparables(server)
    register_rental_yield(server)
    register_neighborhood_analysis(server)
    register_mortgage_calc(server)
    register_investment_report(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
