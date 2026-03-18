"""Tool: calculate_roi"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_calculate_roi(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="calculate_roi",
                description="Calculate Roi - Part of Real Estate Analyzer",
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
        if name == "calculate_roi":
            # TODO: Implement calculate_roi
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "calculate_roi"}  ))]
