"""Tool: docx_to_md"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_docx_to_md(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="docx_to_md",
                description="Docx To Md - Part of Markdown & Doc Converter",
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
        if name == "docx_to_md":
            # TODO: Implement docx_to_md
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "docx_to_md"}  ))]
