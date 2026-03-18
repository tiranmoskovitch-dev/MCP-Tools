"""MCP Server: API Load Tester
HTTP benchmarking, concurrent requests, latency percentiles, reports
Price: $49
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.run_benchmark import register_run_benchmark
from src.tools.concurrent_test import register_concurrent_test
from src.tools.stress_test import register_stress_test
from src.tools.latency_report import register_latency_report
from src.tools.compare_endpoints import register_compare_endpoints
from src.tools.export_results import register_export_results

server = Server("mcp-loadtest")


def register_all_tools():
    register_run_benchmark(server)
    register_concurrent_test(server)
    register_stress_test(server)
    register_latency_report(server)
    register_compare_endpoints(server)
    register_export_results(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
