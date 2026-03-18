"""Tool: generate_palette"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_generate_palette(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="generate_palette",
                description="Generate Palette - Part of Color & Design Tokens",
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
        if name == "generate_palette":
            # TODO: Implement generate_palette
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "generate_palette"}  ))]
