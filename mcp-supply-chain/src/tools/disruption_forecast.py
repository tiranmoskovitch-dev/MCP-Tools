"""Tool: disruption_forecast"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_disruption_forecast(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="disruption_forecast",
                description="Disruption Forecast - Part of Supply Chain Intelligence",
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
        if name == "disruption_forecast":
            # TODO: Implement disruption_forecast
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "disruption_forecast"}  ))]
