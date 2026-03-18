"""Tool: forecast_costs"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_forecast_costs(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="forecast_costs",
                description="Forecast Costs - Part of AWS Cost Optimizer",
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
        if name == "forecast_costs":
            # TODO: Implement forecast_costs
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "forecast_costs"}  ))]
