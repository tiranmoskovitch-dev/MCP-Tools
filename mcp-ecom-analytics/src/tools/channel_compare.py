"""Tool: channel_compare"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_channel_compare(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="channel_compare",
                description="Channel Compare - Part of E-commerce Analytics",
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
        if name == "channel_compare":
            # TODO: Implement channel_compare
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "channel_compare"}  ))]
