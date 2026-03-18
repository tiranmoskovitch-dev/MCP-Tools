"""Tool: hash_file"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_hash_file(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="hash_file",
                description="Hash File - Part of Hash & Crypto Utilities",
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
        if name == "hash_file":
            # TODO: Implement hash_file
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "hash_file"}  ))]
