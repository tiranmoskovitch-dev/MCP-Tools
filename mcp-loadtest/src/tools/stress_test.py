"""Tool: stress_test"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_stress_test(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="stress_test",
                description="Stress Test - Part of API Load Tester",
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
        if name == "stress_test":
            # TODO: Implement stress_test
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "stress_test"}  ))]
