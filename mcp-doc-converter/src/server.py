"""MCP Server: Markdown & Doc Converter
Convert between MD, HTML, PDF, DOCX, RST with table formatting
Price: $29
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.md_to_html import register_md_to_html
from src.tools.md_to_pdf import register_md_to_pdf
from src.tools.html_to_md import register_html_to_md
from src.tools.docx_to_md import register_docx_to_md
from src.tools.generate_toc import register_generate_toc
from src.tools.format_tables import register_format_tables

server = Server("mcp-doc-converter")


def register_all_tools():
    register_md_to_html(server)
    register_md_to_pdf(server)
    register_html_to_md(server)
    register_docx_to_md(server)
    register_generate_toc(server)
    register_format_tables(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
