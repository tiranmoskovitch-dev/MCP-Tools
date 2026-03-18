"""Tool: insider_trades"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_insider_trades(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="insider_trades",
                description="Insider Trades - Part of Stock Sentiment Analyzer",
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
        if name == "insider_trades":
            # TODO: Implement insider_trades
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "insider_trades"}  ))]
