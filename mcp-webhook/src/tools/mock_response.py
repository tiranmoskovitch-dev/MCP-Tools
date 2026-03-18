"""Tool: mock_response"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_mock_response(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="mock_response",
                description="Mock Response - Part of Webhook Tester & Logger",
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
        if name == "mock_response":
            # TODO: Implement mock_response
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "mock_response"}  ))]
