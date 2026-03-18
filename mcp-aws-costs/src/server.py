"""MCP Server: AWS Cost Optimizer
Resource waste detection, reserved instance recommendations, savings
Price: $49
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.cost_breakdown import register_cost_breakdown
from src.tools.waste_detection import register_waste_detection
from src.tools.ri_recommendations import register_ri_recommendations
from src.tools.savings_plan import register_savings_plan
from src.tools.forecast_costs import register_forecast_costs
from src.tools.tag_audit import register_tag_audit

server = Server("mcp-aws-costs")


def register_all_tools():
    register_cost_breakdown(server)
    register_waste_detection(server)
    register_ri_recommendations(server)
    register_savings_plan(server)
    register_forecast_costs(server)
    register_tag_audit(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
