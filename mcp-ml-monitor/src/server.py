"""MCP Server: ML Model Monitor
Model drift detection, prediction quality tracking, feature importance
Price: $79
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.detect_drift import register_detect_drift
from src.tools.prediction_quality import register_prediction_quality
from src.tools.feature_importance import register_feature_importance
from src.tools.ab_compare import register_ab_compare
from src.tools.retrain_trigger import register_retrain_trigger
from src.tools.model_report import register_model_report

server = Server("mcp-ml-monitor")


def register_all_tools():
    register_detect_drift(server)
    register_prediction_quality(server)
    register_feature_importance(server)
    register_ab_compare(server)
    register_retrain_trigger(server)
    register_model_report(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
