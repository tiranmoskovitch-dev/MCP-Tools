"""Tool: fake_address"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_fake_address(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="fake_address",
                description="Fake Address - Part of Lorem & Data Generator",
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
        if name == "fake_address":
            # TODO: Implement fake_address
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "fake_address"}  ))]
