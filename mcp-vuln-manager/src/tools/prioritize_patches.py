"""Tool: prioritize_patches"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_prioritize_patches(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="prioritize_patches",
                description="Prioritize Patches - Part of Vulnerability Manager",
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
        if name == "prioritize_patches":
            # TODO: Implement prioritize_patches
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "prioritize_patches"}  ))]
