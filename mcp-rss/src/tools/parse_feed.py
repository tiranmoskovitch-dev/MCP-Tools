"""Tool: parse_feed"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_parse_feed(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="parse_feed",
                description="Parse Feed - Part of RSS & Feed Aggregator",
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
        if name == "parse_feed":
            # TODO: Implement parse_feed
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "parse_feed"}  ))]
