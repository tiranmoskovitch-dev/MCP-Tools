"""Tool: crawl_site"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_crawl_site(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="crawl_site",
                description="Crawl Site - Part of SEO Site Auditor",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "input": {"type": "string", "description": "Input parameter"}
                    },
                    "required": ["input"]
                }
            )
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        if name == "crawl_site":
            # TODO: Implement crawl_site
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "crawl_site"}  ))]
