"""MCP Server: Revenue Operations
Pipeline forecast, commission calculation, quota tracking, churn prediction
Price: $99
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.pipeline_forecast import register_pipeline_forecast
from src.tools.calculate_commission import register_calculate_commission
from src.tools.quota_tracking import register_quota_tracking
from src.tools.churn_prediction import register_churn_prediction
from src.tools.deal_scoring import register_deal_scoring
from src.tools.revenue_report import register_revenue_report

server = Server("mcp-revops")


def register_all_tools():
    register_pipeline_forecast(server)
    register_calculate_commission(server)
    register_quota_tracking(server)
    register_churn_prediction(server)
    register_deal_scoring(server)
    register_revenue_report(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
