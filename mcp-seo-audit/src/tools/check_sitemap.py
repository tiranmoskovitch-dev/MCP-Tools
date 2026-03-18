"""Tool: check_sitemap"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_check_sitemap(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="check_sitemap",
                description="Check Sitemap - Part of SEO Site Auditor",
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
        if name == "check_sitemap":
            # TODO: Implement check_sitemap
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "check_sitemap"}  ))]
