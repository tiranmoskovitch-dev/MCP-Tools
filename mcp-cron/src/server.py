"""MCP Server: Cron & Schedule Manager
Parse/build cron expressions, next-run calculation, timezone conversion
Price: $29
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.parse_cron import register_parse_cron
from src.tools.build_cron import register_build_cron
from src.tools.next_runs import register_next_runs
from src.tools.cron_explain import register_cron_explain
from src.tools.timezone_convert import register_timezone_convert
from src.tools.schedule_overlap import register_schedule_overlap

server = Server("mcp-cron")


def register_all_tools():
    register_parse_cron(server)
    register_build_cron(server)
    register_next_runs(server)
    register_cron_explain(server)
    register_timezone_convert(server)
    register_schedule_overlap(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
