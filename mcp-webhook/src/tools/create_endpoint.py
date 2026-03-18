"""Tool: create_endpoint"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_create_endpoint(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="create_endpoint",
                description="Create Endpoint - Part of Webhook Tester & Logger",
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
        if name == "create_endpoint":
            # TODO: Implement create_endpoint
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "create_endpoint"}  ))]
