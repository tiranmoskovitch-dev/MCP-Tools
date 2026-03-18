"""MCP Server: CI/CD Pipeline Optimizer
Build time analysis, parallel execution, cache optimization
Price: $79
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.analyze_pipeline import register_analyze_pipeline
from src.tools.find_bottlenecks import register_find_bottlenecks
from src.tools.parallel_strategy import register_parallel_strategy
from src.tools.cache_analysis import register_cache_analysis
from src.tools.build_trends import register_build_trends
from src.tools.optimize_config import register_optimize_config

server = Server("mcp-cicd-optimizer")


def register_all_tools():
    register_analyze_pipeline(server)
    register_find_bottlenecks(server)
    register_parallel_strategy(server)
    register_cache_analysis(server)
    register_build_trends(server)
    register_optimize_config(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
