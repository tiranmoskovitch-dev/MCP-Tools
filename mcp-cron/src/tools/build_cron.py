"""Tool: build_cron"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_build_cron(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="build_cron",
                description="Build Cron - Part of Cron & Schedule Manager",
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
        if name == "build_cron":
            # TODO: Implement build_cron
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "build_cron"}  ))]
