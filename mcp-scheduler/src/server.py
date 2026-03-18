"""MCP Server: Calendar & Scheduling
Multi-timezone scheduling, meeting optimization, availability finder
Price: $49
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.find_availability import register_find_availability
from src.tools.schedule_meeting import register_schedule_meeting
from src.tools.timezone_convert import register_timezone_convert
from src.tools.optimize_schedule import register_optimize_schedule
from src.tools.recurring_events import register_recurring_events
from src.tools.ical_export import register_ical_export

server = Server("mcp-scheduler")


def register_all_tools():
    register_find_availability(server)
    register_schedule_meeting(server)
    register_timezone_convert(server)
    register_optimize_schedule(server)
    register_recurring_events(server)
    register_ical_export(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
