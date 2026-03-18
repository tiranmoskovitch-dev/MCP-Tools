"""Tool: detect_language"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_detect_language(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="detect_language",
                description="Detect Language - Part of Text Analytics",
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
        if name == "detect_language":
            # TODO: Implement detect_language
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "detect_language"}  ))]
