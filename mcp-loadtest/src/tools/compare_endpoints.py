"""Tool: compare_endpoints"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_compare_endpoints(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="compare_endpoints",
                description="Compare Endpoints - Part of API Load Tester",
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
        if name == "compare_endpoints":
            # TODO: Implement compare_endpoints
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "compare_endpoints"}  ))]
