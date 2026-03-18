"""MCP Server: E-commerce Analytics
Multi-channel inventory, dynamic pricing, margin optimization
Price: $79
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.inventory_sync import register_inventory_sync
from src.tools.dynamic_pricing import register_dynamic_pricing
from src.tools.margin_analysis import register_margin_analysis
from src.tools.sales_forecast import register_sales_forecast
from src.tools.channel_compare import register_channel_compare
from src.tools.customer_ltv import register_customer_ltv

server = Server("mcp-ecom-analytics")


def register_all_tools():
    register_inventory_sync(server)
    register_dynamic_pricing(server)
    register_margin_analysis(server)
    register_sales_forecast(server)
    register_channel_compare(server)
    register_customer_ltv(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
