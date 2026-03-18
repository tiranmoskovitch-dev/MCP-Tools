"""Tool: hex_to_rgb"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_hex_to_rgb(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="hex_to_rgb",
                description="Hex To Rgb - Part of Color & Design Tokens",
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
        if name == "hex_to_rgb":
            # TODO: Implement hex_to_rgb
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "hex_to_rgb"}  ))]
