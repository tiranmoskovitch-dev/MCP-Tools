"""Tool: aggregate_feeds"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_aggregate_feeds(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="aggregate_feeds",
                description="Aggregate Feeds - Part of RSS & Feed Aggregator",
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
        if name == "aggregate_feeds":
            # TODO: Implement aggregate_feeds
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "aggregate_feeds"}  ))]
