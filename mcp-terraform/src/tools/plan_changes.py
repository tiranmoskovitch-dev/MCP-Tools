"""Tool: plan_changes"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_plan_changes(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="plan_changes",
                description="Plan Changes - Part of Terraform Manager",
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
        if name == "plan_changes":
            # TODO: Implement plan_changes
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "plan_changes"}  ))]
