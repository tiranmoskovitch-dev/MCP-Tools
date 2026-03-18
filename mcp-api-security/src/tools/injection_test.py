"""Tool: injection_test"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_injection_test(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="injection_test",
                description="Injection Test - Part of API Security Scanner",
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
        if name == "injection_test":
            # TODO: Implement injection_test
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "injection_test"}  ))]
