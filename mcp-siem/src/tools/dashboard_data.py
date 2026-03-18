"""Tool: dashboard_data"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_dashboard_data(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="dashboard_data",
                description="Dashboard Data - Part of Full SIEM Log Platform",
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
        if name == "dashboard_data":
            # TODO: Implement dashboard_data
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "dashboard_data"}  ))]
