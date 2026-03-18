"""Tool: find_matches"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_find_matches(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="find_matches",
                description="Find Matches - Part of Regex Debugger & Generator",
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
        if name == "find_matches":
            # TODO: Implement find_matches
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "find_matches"}  ))]
