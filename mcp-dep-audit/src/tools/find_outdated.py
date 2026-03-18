"""Tool: find_outdated"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_find_outdated(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="find_outdated",
                description="Find Outdated - Part of Dependency Auditor",
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
        if name == "find_outdated":
            # TODO: Implement find_outdated
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "find_outdated"}  ))]
