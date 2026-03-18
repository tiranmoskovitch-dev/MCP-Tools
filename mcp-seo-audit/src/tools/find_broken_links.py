"""Tool: find_broken_links"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_find_broken_links(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="find_broken_links",
                description="Find Broken Links - Part of SEO Site Auditor",
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
        if name == "find_broken_links":
            # TODO: Implement find_broken_links
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "find_broken_links"}  ))]
