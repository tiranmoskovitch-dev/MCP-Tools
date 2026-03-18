"""Tool: inspect_state"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_inspect_state(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="inspect_state",
                description="Inspect State - Part of Terraform Manager",
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
        if name == "inspect_state":
            # TODO: Implement inspect_state
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "inspect_state"}  ))]
