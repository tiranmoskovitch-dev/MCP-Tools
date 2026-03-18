"""Tool: iv_surface"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_iv_surface(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="iv_surface",
                description="Iv Surface - Part of Options Greeks Calculator",
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
        if name == "iv_surface":
            # TODO: Implement iv_surface
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "iv_surface"}  ))]
