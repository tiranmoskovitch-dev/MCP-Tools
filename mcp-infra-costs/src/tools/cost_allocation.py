"""Tool: cost_allocation"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_cost_allocation(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="cost_allocation",
                description="Cost Allocation - Part of Infrastructure Cost Center",
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
        if name == "cost_allocation":
            # TODO: Implement cost_allocation
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "cost_allocation"}  ))]
