"""Tool: cost_estimate"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_cost_estimate(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="cost_estimate",
                description="Cost Estimate - Part of Terraform Manager",
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
        if name == "cost_estimate":
            # TODO: Implement cost_estimate
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "cost_estimate"}  ))]
