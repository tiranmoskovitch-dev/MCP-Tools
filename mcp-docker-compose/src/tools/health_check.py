"""Tool: health_check"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_health_check(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="health_check",
                description="Health Check - Part of Docker Compose Architect",
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
        if name == "health_check":
            # TODO: Implement health_check
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "health_check"}  ))]
