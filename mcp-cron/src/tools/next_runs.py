"""Tool: next_runs"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_next_runs(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="next_runs",
                description="Next Runs - Part of Cron & Schedule Manager",
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
        if name == "next_runs":
            # TODO: Implement next_runs
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "next_runs"}  ))]
