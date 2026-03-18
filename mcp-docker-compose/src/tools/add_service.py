"""Tool: add_service"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_add_service(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="add_service",
                description="Add Service - Part of Docker Compose Architect",
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
        if name == "add_service":
            # TODO: Implement add_service
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "add_service"}  ))]
