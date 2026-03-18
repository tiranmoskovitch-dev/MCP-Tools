"""Tool: generate_key"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_generate_key(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="generate_key",
                description="Generate Key - Part of Hash & Crypto Utilities",
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
        if name == "generate_key":
            # TODO: Implement generate_key
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "generate_key"}  ))]
