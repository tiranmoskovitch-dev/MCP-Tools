"""Tool: hash_text"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_hash_text(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="hash_text",
                description="Hash Text - Part of Hash & Crypto Utilities",
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
        if name == "hash_text":
            # TODO: Implement hash_text
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "hash_text"}  ))]
