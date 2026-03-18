"""Tool: savings_plan"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_savings_plan(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="savings_plan",
                description="Savings Plan - Part of AWS Cost Optimizer",
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
        if name == "savings_plan":
            # TODO: Implement savings_plan
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "savings_plan"}  ))]
