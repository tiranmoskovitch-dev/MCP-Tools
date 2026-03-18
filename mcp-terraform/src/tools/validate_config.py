"""Tool: validate_config"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_validate_config(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="validate_config",
                description="Validate Config - Part of Terraform Manager",
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
        if name == "validate_config":
            # TODO: Implement validate_config
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "validate_config"}  ))]
