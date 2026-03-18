"""Tool: schedule_overlap"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_schedule_overlap(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="schedule_overlap",
                description="Schedule Overlap - Part of Cron & Schedule Manager",
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
        if name == "schedule_overlap":
            # TODO: Implement schedule_overlap
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "schedule_overlap"}  ))]
