"""MCP Server: Email Campaign Builder
Template builder, A/B test analyzer, deliverability optimizer
Price: $49
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.build_template import register_build_template
from src.tools.ab_test_analyze import register_ab_test_analyze
from src.tools.preview_render import register_preview_render
from src.tools.subject_line_score import register_subject_line_score
from src.tools.list_hygiene import register_list_hygiene
from src.tools.send_test import register_send_test

server = Server("mcp-email-campaign")


def register_all_tools():
    register_build_template(server)
    register_ab_test_analyze(server)
    register_preview_render(server)
    register_subject_line_score(server)
    register_list_hygiene(server)
    register_send_test(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
