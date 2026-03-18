"""Tool: pnl_analysis"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_pnl_analysis(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="pnl_analysis",
                description="Pnl Analysis - Part of Crypto Portfolio Tracker",
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
        if name == "pnl_analysis":
            # TODO: Implement pnl_analysis
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "pnl_analysis"}  ))]
