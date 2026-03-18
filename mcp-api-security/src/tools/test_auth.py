"""Tool: test_auth"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_test_auth(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="test_auth",
                description="Test Auth - Part of API Security Scanner",
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
        if name == "test_auth":
            # TODO: Implement test_auth
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "test_auth"}  ))]
