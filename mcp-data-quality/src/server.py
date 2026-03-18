"""MCP Server: Data Quality Monitor
Anomaly detection, missing data patterns, schema drift, profiling
Price: $79
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.profile_dataset import register_profile_dataset
from src.tools.detect_anomalies import register_detect_anomalies
from src.tools.check_completeness import register_check_completeness
from src.tools.schema_drift import register_schema_drift
from src.tools.quality_score import register_quality_score
from src.tools.validation_rules import register_validation_rules

server = Server("mcp-data-quality")


def register_all_tools():
    register_profile_dataset(server)
    register_detect_anomalies(server)
    register_check_completeness(server)
    register_schema_drift(server)
    register_quality_score(server)
    register_validation_rules(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
