"""Tool: forecast_spend"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_forecast_spend(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="forecast_spend",
                description="Forecast Spend - Part of Infrastructure Cost Center",
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
        if name == "forecast_spend":
            # TODO: Implement forecast_spend
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "forecast_spend"}  ))]
