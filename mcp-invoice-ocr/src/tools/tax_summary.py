"""Tool: tax_summary"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_tax_summary(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="tax_summary",
                description="Tax Summary - Part of Invoice & Receipt OCR",
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
        if name == "tax_summary":
            # TODO: Implement tax_summary
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "tax_summary"}  ))]
