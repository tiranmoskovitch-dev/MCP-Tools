"""Tool: build_strategy"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_build_strategy(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="build_strategy",
                description="Build Strategy - Part of Options Greeks Calculator",
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
        if name == "build_strategy":
            # TODO: Implement build_strategy
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "build_strategy"}  ))]
