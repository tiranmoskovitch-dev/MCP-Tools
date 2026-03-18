"""MCP Server: Infrastructure Cost Center
Multi-cloud cost analysis, FinOps dashboards, budget alerts
Price: $99
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.cost_analysis import register_cost_analysis
from src.tools.budget_alerts import register_budget_alerts
from src.tools.resource_optimize import register_resource_optimize
from src.tools.forecast_spend import register_forecast_spend
from src.tools.tag_compliance import register_tag_compliance
from src.tools.cost_allocation import register_cost_allocation

server = Server("mcp-infra-costs")


def register_all_tools():
    register_cost_analysis(server)
    register_budget_alerts(server)
    register_resource_optimize(server)
    register_forecast_spend(server)
    register_tag_compliance(server)
    register_cost_allocation(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
