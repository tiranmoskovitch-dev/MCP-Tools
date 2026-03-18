"""MCP Server: Color & Design Tokens
Palette generation, contrast checker, WCAG compliance, theme builder
Price: $29
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.generate_palette import register_generate_palette
from src.tools.check_contrast import register_check_contrast
from src.tools.wcag_compliance import register_wcag_compliance
from src.tools.hex_to_rgb import register_hex_to_rgb
from src.tools.color_harmonies import register_color_harmonies
from src.tools.build_theme import register_build_theme

server = Server("mcp-color-tools")


def register_all_tools():
    register_generate_palette(server)
    register_check_contrast(server)
    register_wcag_compliance(server)
    register_hex_to_rgb(server)
    register_color_harmonies(server)
    register_build_theme(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
