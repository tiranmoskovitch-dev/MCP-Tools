"""MCP Server: Regex Debugger & Generator
Build, test, explain regexes, generate patterns from examples
Price: $29
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.test_regex import register_test_regex
from src.tools.explain_regex import register_explain_regex
from src.tools.generate_regex import register_generate_regex
from src.tools.find_matches import register_find_matches
from src.tools.replace_with_regex import register_replace_with_regex
from src.tools.validate_pattern import register_validate_pattern

server = Server("mcp-regex")


def register_all_tools():
    register_test_regex(server)
    register_explain_regex(server)
    register_generate_regex(server)
    register_find_matches(server)
    register_replace_with_regex(server)
    register_validate_pattern(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
