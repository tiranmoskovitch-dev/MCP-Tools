"""Tool: explain_regex"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_explain_regex(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="explain_regex",
                description="Explain Regex - Part of Regex Debugger & Generator",
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
        if name == "explain_regex":
            # TODO: Implement explain_regex
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "explain_regex"}  ))]
