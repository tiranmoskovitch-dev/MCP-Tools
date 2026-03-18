"""MCP Server: Data Pipeline Orchestrator
ETL workflows, scheduling, monitoring, retry logic, lineage
Price: $99
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.create_pipeline import register_create_pipeline
from src.tools.run_pipeline import register_run_pipeline
from src.tools.monitor_jobs import register_monitor_jobs
from src.tools.retry_failed import register_retry_failed
from src.tools.data_lineage import register_data_lineage
from src.tools.schedule_pipeline import register_schedule_pipeline
from src.tools.pipeline_stats import register_pipeline_stats

server = Server("mcp-data-pipeline")


def register_all_tools():
    register_create_pipeline(server)
    register_run_pipeline(server)
    register_monitor_jobs(server)
    register_retry_failed(server)
    register_data_lineage(server)
    register_schedule_pipeline(server)
    register_pipeline_stats(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
