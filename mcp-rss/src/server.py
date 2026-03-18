"""MCP Server: RSS & Feed Aggregator
Parse feeds, aggregate, filter by keywords, OPML import
Price: $29
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.parse_feed import register_parse_feed
from src.tools.aggregate_feeds import register_aggregate_feeds
from src.tools.filter_entries import register_filter_entries
from src.tools.import_opml import register_import_opml
from src.tools.export_opml import register_export_opml
from src.tools.keyword_alerts import register_keyword_alerts

server = Server("mcp-rss")


def register_all_tools():
    register_parse_feed(server)
    register_aggregate_feeds(server)
    register_filter_entries(server)
    register_import_opml(server)
    register_export_opml(server)
    register_keyword_alerts(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
