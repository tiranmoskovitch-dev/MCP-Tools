"""Tool: generate_regex"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_generate_regex(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="generate_regex",
                description="Generate Regex - Part of Regex Debugger & Generator",
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
        if name == "generate_regex":
            # TODO: Implement generate_regex
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "generate_regex"}  ))]
