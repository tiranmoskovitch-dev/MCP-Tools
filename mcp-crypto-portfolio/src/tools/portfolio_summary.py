"""Tool: portfolio_summary"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_portfolio_summary(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="portfolio_summary",
                description="Portfolio Summary - Part of Crypto Portfolio Tracker",
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
        if name == "portfolio_summary":
            # TODO: Implement portfolio_summary
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "portfolio_summary"}  ))]
