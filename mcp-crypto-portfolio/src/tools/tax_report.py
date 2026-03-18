"""Tool: tax_report"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_tax_report(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="tax_report",
                description="Tax Report - Part of Crypto Portfolio Tracker",
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
        if name == "tax_report":
            # TODO: Implement tax_report
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "tax_report"}  ))]
