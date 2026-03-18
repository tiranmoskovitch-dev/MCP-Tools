"""Tool: ab_compare"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_ab_compare(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="ab_compare",
                description="Ab Compare - Part of ML Model Monitor",
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
        if name == "ab_compare":
            # TODO: Implement ab_compare
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "ab_compare"}  ))]
