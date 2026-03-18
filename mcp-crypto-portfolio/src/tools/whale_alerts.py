"""Tool: whale_alerts"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_whale_alerts(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="whale_alerts",
                description="Whale Alerts - Part of Crypto Portfolio Tracker",
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
        if name == "whale_alerts":
            # TODO: Implement whale_alerts
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "whale_alerts"}  ))]
