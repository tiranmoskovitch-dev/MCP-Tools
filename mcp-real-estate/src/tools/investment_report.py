"""Tool: investment_report"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_investment_report(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="investment_report",
                description="Investment Report - Part of Real Estate Analyzer",
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
        if name == "investment_report":
            # TODO: Implement investment_report
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "investment_report"}  ))]
