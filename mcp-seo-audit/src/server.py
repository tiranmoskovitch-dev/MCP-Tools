"""MCP Server: SEO Site Auditor
Crawl site, Core Web Vitals, structured data, broken links
Price: $49
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.crawl_site import register_crawl_site
from src.tools.check_vitals import register_check_vitals
from src.tools.validate_schema import register_validate_schema
from src.tools.find_broken_links import register_find_broken_links
from src.tools.check_sitemap import register_check_sitemap
from src.tools.seo_score import register_seo_score

server = Server("mcp-seo-audit")


def register_all_tools():
    register_crawl_site(server)
    register_check_vitals(server)
    register_validate_schema(server)
    register_find_broken_links(server)
    register_check_sitemap(server)
    register_seo_score(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
