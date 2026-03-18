"""Tool: list_requests"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_list_requests(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="list_requests",
                description="List Requests - Part of Webhook Tester & Logger",
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
        if name == "list_requests":
            # TODO: Implement list_requests
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "list_requests"}  ))]
