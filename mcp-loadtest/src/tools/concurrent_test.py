"""Tool: concurrent_test"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_concurrent_test(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="concurrent_test",
                description="Concurrent Test - Part of API Load Tester",
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
        if name == "concurrent_test":
            # TODO: Implement concurrent_test
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "concurrent_test"}  ))]
