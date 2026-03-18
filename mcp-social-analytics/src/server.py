"""MCP Server: Social Media Analytics
Post performance, hashtag analysis, optimal timing, competitors
Price: $49
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.analyze_post import register_analyze_post
from src.tools.hashtag_research import register_hashtag_research
from src.tools.optimal_timing import register_optimal_timing
from src.tools.competitor_compare import register_competitor_compare
from src.tools.engagement_report import register_engagement_report
from src.tools.trend_detect import register_trend_detect

server = Server("mcp-social-analytics")


def register_all_tools():
    register_analyze_post(server)
    register_hashtag_research(server)
    register_optimal_timing(server)
    register_competitor_compare(server)
    register_engagement_report(server)
    register_trend_detect(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
