"""MCP Server: Supply Chain Intelligence
Supplier risk scoring, disruption forecasting, lead time optimization
Price: $99
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.supplier_risk import register_supplier_risk
from src.tools.disruption_forecast import register_disruption_forecast
from src.tools.lead_time_optimize import register_lead_time_optimize
from src.tools.inventory_optimize import register_inventory_optimize
from src.tools.cost_analysis import register_cost_analysis
from src.tools.supply_report import register_supply_report

server = Server("mcp-supply-chain")


def register_all_tools():
    register_supplier_risk(server)
    register_disruption_forecast(server)
    register_lead_time_optimize(server)
    register_inventory_optimize(server)
    register_cost_analysis(server)
    register_supply_report(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
