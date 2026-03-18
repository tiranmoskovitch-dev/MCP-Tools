"""Tool: test_regex"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_test_regex(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="test_regex",
                description="Test Regex - Part of Regex Debugger & Generator",
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
        if name == "test_regex":
            # TODO: Implement test_regex
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "test_regex"}  ))]
