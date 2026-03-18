"""Tool: latency_report"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_latency_report(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="latency_report",
                description="Latency Report - Part of API Load Tester",
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
        if name == "latency_report":
            # TODO: Implement latency_report
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "latency_report"}  ))]
