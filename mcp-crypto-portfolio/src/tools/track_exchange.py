"""Tool: track_exchange"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_track_exchange(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="track_exchange",
                description="Track Exchange - Part of Crypto Portfolio Tracker",
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
        if name == "track_exchange":
            # TODO: Implement track_exchange
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "track_exchange"}  ))]
