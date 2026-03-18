"""Tool: cron_explain"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_cron_explain(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="cron_explain",
                description="Cron Explain - Part of Cron & Schedule Manager",
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
        if name == "cron_explain":
            # TODO: Implement cron_explain
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "cron_explain"}  ))]
