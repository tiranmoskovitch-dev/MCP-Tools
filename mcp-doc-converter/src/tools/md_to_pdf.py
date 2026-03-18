"""Tool: md_to_pdf"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_md_to_pdf(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="md_to_pdf",
                description="Md To Pdf - Part of Markdown & Doc Converter",
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
        if name == "md_to_pdf":
            # TODO: Implement md_to_pdf
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "md_to_pdf"}  ))]
