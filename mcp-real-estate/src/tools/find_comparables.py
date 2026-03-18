"""Tool: find_comparables"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_find_comparables(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="find_comparables",
                description="Find Comparables - Part of Real Estate Analyzer",
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
        if name == "find_comparables":
            # TODO: Implement find_comparables
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "find_comparables"}  ))]
