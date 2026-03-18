"""Tool: replace_with_regex"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_replace_with_regex(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="replace_with_regex",
                description="Replace With Regex - Part of Regex Debugger & Generator",
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
        if name == "replace_with_regex":
            # TODO: Implement replace_with_regex
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "replace_with_regex"}  ))]
