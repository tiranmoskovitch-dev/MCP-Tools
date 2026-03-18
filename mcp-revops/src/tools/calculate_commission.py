"""Tool: calculate_commission"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_calculate_commission(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="calculate_commission",
                description="Calculate Commission - Part of Revenue Operations",
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
        if name == "calculate_commission":
            # TODO: Implement calculate_commission
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "calculate_commission"}  ))]
