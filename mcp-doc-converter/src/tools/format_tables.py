"""Tool: format_tables"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_format_tables(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="format_tables",
                description="Format Tables - Part of Markdown & Doc Converter",
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
        if name == "format_tables":
            # TODO: Implement format_tables
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "format_tables"}  ))]
