"""Tool: cost_breakdown"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_cost_breakdown(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="cost_breakdown",
                description="Cost Breakdown - Part of AWS Cost Optimizer",
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
        if name == "cost_breakdown":
            # TODO: Implement cost_breakdown
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "cost_breakdown"}  ))]
