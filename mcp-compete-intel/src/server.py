"""MCP Server: Competitive Intelligence
Track competitor websites, pricing changes, tech stack detection
Price: $49
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.detect_tech_stack import register_detect_tech_stack
from src.tools.track_changes import register_track_changes
from src.tools.pricing_monitor import register_pricing_monitor
from src.tools.compare_features import register_compare_features
from src.tools.traffic_estimate import register_traffic_estimate
from src.tools.social_presence import register_social_presence

server = Server("mcp-compete-intel")


def register_all_tools():
    register_detect_tech_stack(server)
    register_track_changes(server)
    register_pricing_monitor(server)
    register_compare_features(server)
    register_traffic_estimate(server)
    register_social_presence(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
