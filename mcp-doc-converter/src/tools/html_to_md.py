"""Tool: html_to_md"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_html_to_md(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="html_to_md",
                description="Html To Md - Part of Markdown & Doc Converter",
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
        if name == "html_to_md":
            # TODO: Implement html_to_md
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "html_to_md"}  ))]
