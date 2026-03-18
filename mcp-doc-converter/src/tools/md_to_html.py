"""Tool: md_to_html"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_md_to_html(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="md_to_html",
                description="Md To Html - Part of Markdown & Doc Converter",
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
        if name == "md_to_html":
            # TODO: Implement md_to_html
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "md_to_html"}  ))]
