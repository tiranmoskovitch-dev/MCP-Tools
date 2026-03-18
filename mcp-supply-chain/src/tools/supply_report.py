"""Tool: supply_report"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_supply_report(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="supply_report",
                description="Supply Report - Part of Supply Chain Intelligence",
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
        if name == "supply_report":
            # TODO: Implement supply_report
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "supply_report"}  ))]
